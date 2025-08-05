import streamlit as st
import docx2txt
import PyPDF2
import logging
import re
import requests
import json
from typing import Dict, Any, List
from collections import Counter
import time

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ATSChecker:
    def __init__(self):
        self.setup_page()
        self.ats_standards = self.load_ats_standards()
        
    def setup_page(self):
        """Setup the ATS Checker page configuration"""
        st.title("🎯 Professional ATS Resume Checker")
        st.markdown("**Advanced AI-powered resume analysis following real ATS standards**")
        st.info("🤖 Using LLM for comprehensive resume evaluation")
    
    def load_ats_standards(self):
        """Load strict ATS standards for accurate scoring"""
        return {
            "critical_sections": ["contact", "experience", "skills"],
            "scoring_thresholds": {
                "excellent": 80,      # Very rare - top 5% of resumes
                "good": 65,          # Good - top 20% of resumes  
                "average": 45,       # Average - most resumes fall here
                "poor": 25,          # Poor - needs major work
                "fail": 0            # Fail - fundamental issues
            },
            "keyword_weights": {
                "exact_match": 3,     # Exact job requirement match
                "related_match": 2,   # Related/similar skill
                "partial_match": 1    # Partially relevant
            },
            "formatting_penalties": {
                "no_contact_info": -15,
                "poor_structure": -10,
                "ats_incompatible": -20,
                "spelling_errors": -5,
                "no_experience_section": -25,
                "no_skills_section": -10
            }
        }

    def query_groq_llm(self, prompt: str) -> str:
        """Query Groq's free LLM API"""
        try:
            # Groq offers free API with good models
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": "Bearer gsk_YOUR_FREE_API_KEY",  # Get free key from groq.com
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",  # Free model
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self.fallback_analysis(prompt)
                
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return self.fallback_analysis(prompt)

    def query_huggingface_llm(self, prompt: str) -> str:
        """Query Hugging Face free inference API"""
        try:
            models = [
                "microsoft/DialoGPT-medium",
                "facebook/blenderbot-400M-distill",
                "google/flan-t5-large"
            ]
            
            for model in models:
                try:
                    response = requests.post(
                        f"https://api-inference.huggingface.co/models/{model}",
                        headers={"Authorization": "Bearer hf_YOUR_FREE_TOKEN"},
                        json={"inputs": prompt[:1200], "parameters": {"max_new_tokens": 500}},
                        timeout=25
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get("generated_text", "")
                        return str(result)
                except:
                    continue
            
            return self.fallback_analysis(prompt)
            
        except Exception as e:
            logger.error(f"HuggingFace error: {str(e)}")
            return self.fallback_analysis(prompt)

    def get_llm_analysis(self, resume_text: str, job_description: str) -> str:
        """Get comprehensive LLM analysis with resume-specific prompts"""
        
        # Specialized prompt for resume analysis
        prompt = f"""You are an expert ATS (Applicant Tracking System) resume analyzer and HR professional. 

TASK: Analyze this resume against the job description and provide a detailed assessment.

RESUME TO ANALYZE:
{resume_text[:2500]}

JOB DESCRIPTION:
{job_description[:2000]}

ANALYSIS REQUIREMENTS:
1. **Resume Quality Assessment** (Be strict and realistic):
   - Is this actually a well-formatted resume?
   - Does it have proper sections (Contact, Experience, Skills, Education)?
   - Are achievements quantified with numbers/metrics?
   - Is the language professional and error-free?

2. **ATS Compatibility Issues**:
   - Any formatting problems that would break ATS parsing?
   - Missing critical information (contact details, dates, etc.)?
   - Poor keyword optimization?

3. **Job Match Analysis**:
   - What percentage of job requirements does this resume meet? (Be realistic - most resumes meet 30-60%)
   - Which critical skills are missing?
   - How well does experience align with job level?

4. **Specific Improvement Areas**:
   - What are the top 3 critical fixes needed?
   - Which keywords should be added?
   - How can the candidate better demonstrate qualifications?

IMPORTANT: Be honest and critical. A typical resume should score 35-55 out of 100. Only exceptional resumes that perfectly match job requirements should score above 70.

Provide your analysis in this format:
### Resume Quality: [Score/10]
[Your assessment]

### ATS Compatibility: [Score/10] 
[Your assessment]

### Job Match: [Score/10]
[Your assessment]

### Critical Issues:
- [Issue 1]
- [Issue 2] 
- [Issue 3]

### Recommendations:
1. [Specific actionable advice]
2. [Specific actionable advice]
3. [Specific actionable advice]

### Estimated ATS Score: [XX/100]
[Brief justification for score]"""

        # Try multiple LLM services
        analysis = self.query_groq_llm(prompt)
        if not analysis or len(analysis) < 100:
            analysis = self.query_huggingface_llm(prompt)
        if not analysis or len(analysis) < 100:
            analysis = self.fallback_analysis(prompt)
            
        return analysis

    def fallback_analysis(self, prompt: str) -> str:
        """Intelligent rule-based analysis when LLM fails"""
        # Extract resume and job from prompt
        parts = prompt.split("JOB DESCRIPTION:")
        if len(parts) != 2:
            return "Unable to analyze resume structure."
            
        resume_text = parts[0].split("RESUME TO ANALYZE:")[1].strip()
        job_description = parts[1].split("ANALYSIS REQUIREMENTS:")[0].strip()
        
        return self.advanced_rule_based_analysis(resume_text, job_description)

    def advanced_rule_based_analysis(self, resume_text: str, job_description: str) -> str:
        """Advanced rule-based analysis with realistic scoring"""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Critical resume components check
        has_contact = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text))
        has_phone = bool(re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', resume_text))
        has_experience = any(word in resume_lower for word in ['experience', 'work', 'employment', 'developer', 'engineer', 'analyst'])
        has_skills = any(word in resume_lower for word in ['skills', 'technologies', 'programming', 'software'])
        
        # Experience analysis
        experience_years = re.findall(r'(\d+)\+?\s*years?', resume_lower)
        resume_years = max([int(x) for x in experience_years]) if experience_years else 0
        
        job_years = re.findall(r'(\d+)\+?\s*years?', job_lower)
        required_years = max([int(x) for x in job_years]) if job_years else 3
        
        # Technical skills matching (more comprehensive)
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
            'kubernetes', 'git', 'agile', 'scrum', 'api', 'database', 'frontend', 
            'backend', 'fullstack', 'microservices', 'devops', 'ci/cd'
        ]
        
        job_tech_keywords = [kw for kw in tech_keywords if kw in job_lower]
        resume_tech_keywords = [kw for kw in job_tech_keywords if kw in resume_lower]
        
        # Calculate realistic scores
        resume_quality = 5  # Start with base score
        if has_contact: resume_quality += 1
        if has_phone: resume_quality += 1
        if has_experience: resume_quality += 2
        if has_skills: resume_quality += 1
        
        ats_compatibility = 6  # Start with base
        if not has_contact: ats_compatibility -= 2
        if not has_experience: ats_compatibility -= 3
        if len(resume_text.split()) < 100: ats_compatibility -= 2
        
        # Job match calculation (be realistic)
        if job_tech_keywords:
            match_percentage = len(resume_tech_keywords) / len(job_tech_keywords)
            job_match = min(8, int(match_percentage * 10))
        else:
            job_match = 5
            
        # Experience match
        if resume_years >= required_years:
            job_match = min(job_match + 1, 8)
        elif resume_years >= required_years * 0.7:
            pass  # No penalty
        else:
            job_match = max(job_match - 2, 2)
        
        # Calculate final score (realistic range: 20-70)
        final_score = int((resume_quality * 2 + ats_compatibility * 2 + job_match * 6) * 1.2)
        final_score = max(15, min(75, final_score))  # Cap between 15-75
        
        # Generate analysis
        critical_issues = []
        if not has_contact: critical_issues.append("Missing email address")
        if not has_experience: critical_issues.append("No clear work experience section")
        if len(resume_tech_keywords) < len(job_tech_keywords) * 0.3:
            critical_issues.append("Insufficient technical keyword matches")
        
        missing_keywords = [kw for kw in job_tech_keywords if kw not in resume_tech_keywords]
        
        analysis = f"""### Resume Quality: {resume_quality}/10
Resume structure is {'adequate' if resume_quality >= 6 else 'poor'} with {'proper' if has_experience and has_skills else 'missing'} essential sections.

### ATS Compatibility: {ats_compatibility}/10
{'Good' if ats_compatibility >= 7 else 'Issues with'} ATS parsing potential due to {'standard formatting' if has_contact and has_experience else 'missing critical elements'}.

### Job Match: {job_match}/10
Matches {len(resume_tech_keywords)}/{len(job_tech_keywords)} required technical skills ({int(len(resume_tech_keywords)/max(1,len(job_tech_keywords))*100)}% match rate).

### Critical Issues:
{chr(10).join(f'- {issue}' for issue in critical_issues[:3]) if critical_issues else '- No major structural issues found'}

### Recommendations:
1. Add missing keywords: {', '.join(missing_keywords[:5]) if missing_keywords else 'Focus on quantifying achievements'}
2. {'Include contact information' if not has_contact else 'Improve technical skills section'}
3. {'Add work experience section' if not has_experience else 'Better align experience with job requirements'}

### Estimated ATS Score: {final_score}/100
{'Below average' if final_score < 45 else 'Average' if final_score < 65 else 'Good'} score reflecting realistic ATS standards where most resumes score 30-60."""
        
        return analysis

    def extract_text_from_resume(self, uploaded_file):
        """Extract text from uploaded resume file"""
        text = ""
        if uploaded_file is not None:
            try:
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
                elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                    text = docx2txt.process(uploaded_file)
                else:
                    st.error("⚠️ Please upload PDF or DOCX files only.")
                    return ""
            except Exception as e:
                logger.error(f"Error extracting text: {str(e)}")
                st.error("❌ File extraction failed. Please check file format.")
        return text

    def calculate_realistic_ats_score(self, resume_text: str, job_description: str, llm_analysis: str) -> Dict[str, Any]:
        """Calculate realistic ATS score based on actual standards"""
        
        # Extract LLM scores if available
        llm_score = 35  # Default realistic score
        try:
            score_match = re.search(r'ATS Score:?\s*(\d+)', llm_analysis, re.IGNORECASE)
            if score_match:
                llm_score = int(score_match.group(1))
                # Ensure realistic range
                llm_score = max(10, min(85, llm_score))
        except:
            pass
        
        # Additional checks for score validation
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Penalty factors
        penalties = 0
        
        # Missing critical elements
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            penalties += 15
        
        if not any(word in resume_lower for word in ['experience', 'work', 'employment']):
            penalties += 25
            
        if len(resume_text.split()) < 150:  # Too short
            penalties += 20
            
        # Apply realistic scoring
        final_score = max(5, llm_score - penalties)
        
        # Score categorization (realistic)
        if final_score >= 75:
            category = "Excellent"
            color = "#4CAF50"
        elif final_score >= 60:
            category = "Good" 
            color = "#2196F3"
        elif final_score >= 40:
            category = "Average"
            color = "#FF9800"
        elif final_score >= 25:
            category = "Poor"
            color = "#FF5722"
        else:
            category = "Needs Major Work"
            color = "#F44336"
        
        return {
            "score": final_score,
            "category": category,
            "color": color,
            "penalties": penalties,
            "realistic_range": self.get_realistic_score_explanation(final_score)
        }

    def get_realistic_score_explanation(self, score: int) -> str:
        """Provide realistic score context"""
        if score >= 75:
            return "🏆 Top 5% of resumes - Exceptional match with strong ATS optimization"
        elif score >= 60:
            return "⭐ Top 20% of resumes - Good match with minor improvements needed"
        elif score >= 40:
            return "📊 Average resume - Typical score, room for significant improvement"
        elif score >= 25:
            return "⚠️ Below average - Major improvements required for ATS success"
        else:
            return "🚨 Critical issues - Fundamental resume problems need immediate attention"

    def display_analysis_results(self, llm_analysis: str, ats_score_data: Dict[str, Any]):
        """Display comprehensive analysis results"""
        
        # Main score display
        score = ats_score_data["score"]
        category = ats_score_data["category"]
        color = ats_score_data["color"]
        
        st.subheader("🎯 ATS Compatibility Analysis")
        
        # Score visualization
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #f0f0f0 0%, #f0f0f0 100%); 
                        border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <div style="background: linear-gradient(90deg, {color} 0%, {color} {score}%, #e0e0e0 {score}%, #e0e0e0 100%); 
                            height: 35px; border-radius: 8px; display: flex; align-items: center; 
                            justify-content: center; color: white; font-weight: bold; font-size: 18px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    {score}/100
                </div>
                <div style="text-align: center; margin-top: 10px; font-weight: bold; color: {color};">
                    {category}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("ATS Score", f"{score}/100")
            
        with col3:
            st.metric("Percentile", category)
        
        # Realistic score context
        st.info(f"**Score Context:** {ats_score_data['realistic_range']}")
        
        # LLM Analysis Results
        st.subheader("🤖 Detailed AI Analysis")
        
        # Parse and display LLM analysis
        if "###" in llm_analysis:
            sections = llm_analysis.split("###")
            for section in sections[1:]:  # Skip first empty section
                if section.strip():
                    lines = section.strip().split('\n')
                    if lines:
                        section_title = lines[0].strip()
                        section_content = '\n'.join(lines[1:]).strip()
                        
                        with st.expander(f"📋 {section_title}", expanded=True):
                            st.markdown(section_content)
        else:
            st.markdown(llm_analysis)
        
        # Score breakdown
        st.subheader("📊 Score Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### ⚖️ Scoring Standards")
            st.markdown("""
            - **75-85**: Exceptional (Top 5%)
            - **60-74**: Good (Top 20%) 
            - **40-59**: Average (Most resumes)
            - **25-39**: Below Average
            - **0-24**: Critical Issues
            """)
            
        with col2:
            st.markdown("### 🎯 Your Score Factors")
            penalties = ats_score_data.get("penalties", 0)
            if penalties > 0:
                st.markdown(f"**Penalties Applied**: -{penalties} points")
                st.markdown("**Common penalties:**")
                st.markdown("- Missing contact info: -15")
                st.markdown("- No experience section: -25") 
                st.markdown("- Too short/brief: -20")
            else:
                st.markdown("✅ **No major penalties detected**")

    def show(self):
        """Main application interface"""
        
        # Sidebar with realistic ATS info
        with st.sidebar:
            st.header("📈 ATS Reality Check")
            
            st.markdown("""
            ### 🎯 Realistic Score Distribution
            - **75-85%**: Top 5% of resumes
            - **60-74%**: Top 20% of resumes  
            - **40-59%**: Average (most resumes)
            - **25-39%**: Below average
            - **0-24%**: Major issues
            """)
            
            st.markdown("---")
            
            with st.expander("❌ Why Most Resumes Score Low"):
                st.markdown("""
                **Reality**: 70% of resumes score 30-50
                
                **Common Issues:**
                - Generic, not tailored to job
                - Missing key technical skills
                - Poor formatting/structure
                - Lack of quantified achievements
                - No clear value proposition
                """)
            
            with st.expander("✅ High-Scoring Resume Traits"):
                st.markdown("""
                **Top 20% resumes have:**
                - 80%+ keyword match with job
                - Quantified achievements
                - Perfect ATS formatting
                - Relevant experience levels
                - Industry-specific language
                """)
        
        # Main interface
        st.markdown("## Resume Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📄 Upload Resume")
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=["pdf", "docx"],
                help="PDF or DOCX format recommended"
            )
            
            # Demo toggle
            use_demo = st.checkbox("📋 Use demo data")
            
            if use_demo:
                demo_resume = st.text_area(
                    "Demo Resume", 
                    height=300,
                    value="""John Smith
Software Developer
john.smith@email.com | (555) 123-4567

EXPERIENCE:
Software Developer at TechCorp (2021-Present)
- Built web applications using React and Node.js
- Worked with databases and APIs
- Collaborated with team members

Junior Developer at StartupXYZ (2019-2021)  
- Developed features for mobile app
- Fixed bugs and improved performance

SKILLS:
JavaScript, React, Node.js, SQL, Git

EDUCATION:
Computer Science Degree, University (2019)"""
                )
        
        with col2:
            st.markdown("### 💼 Job Description")
            job_description = st.text_area(
                "Paste the complete job description",
                height=400,
                placeholder="Include all requirements, qualifications, and responsibilities..."
            )
            
            if use_demo and not job_description:
                demo_job = st.text_area(
                    "Demo Job Description",
                    height=300,
                    value="""Senior Full Stack Developer

REQUIREMENTS:
• 5+ years experience in full stack development
• Expert in JavaScript, TypeScript, React, Node.js
• Strong experience with Python and Django/Flask
• Proficient in SQL databases (PostgreSQL, MySQL)
• AWS cloud services experience required
• Docker and Kubernetes knowledge
• Git version control and CI/CD pipelines
• Agile/Scrum methodology experience
• Strong problem-solving and communication skills

PREFERRED:
• Leadership experience
• Machine learning knowledge  
• DevOps experience
• Open source contributions"""
                )
                job_description = demo_job
        
        # Analysis button
        if st.button("🔍 Analyze Resume with AI", type="primary", use_container_width=True):
            if not job_description.strip():
                st.error("⚠️ Please provide a job description for accurate analysis")
                return
                
            if not uploaded_file and not use_demo:
                st.error("⚠️ Please upload a resume or use demo data")
                return
            
            with st.spinner("🤖 AI is analyzing your resume... This may take 30-60 seconds"):
                try:
                    # Extract resume text
                    if use_demo:
                        resume_text = demo_resume
                    else:
                        resume_text = self.extract_text_from_resume(uploaded_file)
                    
                    if not resume_text.strip():
                        st.error("❌ Could not extract text from resume file")
                        return
                    
                    # Get comprehensive LLM analysis
                    llm_analysis = self.get_llm_analysis(resume_text, job_description)
                    
                    # Calculate realistic ATS score
                    ats_score_data = self.calculate_realistic_ats_score(
                        resume_text, job_description, llm_analysis
                    )
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    self.display_analysis_results(llm_analysis, ats_score_data)
                    
                    # Additional tips based on score
                    score = ats_score_data["score"]
                    
                    st.markdown("---")
                    if score < 40:
                        st.error("🚨 **Critical Action Required**")
                        with st.expander("Immediate Improvements Needed"):
                            st.markdown("""
                            **Priority 1 - Fix These Now:**
                            1. Add complete contact information
                            2. Create proper Experience section with dates
                            3. Add Skills section with job-relevant technologies  
                            4. Quantify achievements with numbers
                            5. Match job keywords exactly as written
                            """)
                    elif score < 60:
                        st.warning("⚠️ **Good Foundation, Needs Optimization**")
                        with st.expander("Improvement Strategies"):
                            st.markdown("""
                            **Next Steps:**
                            1. Add missing technical keywords from job description
                            2. Quantify all achievements with metrics
                            3. Tailor experience descriptions to match job requirements
                            4. Add relevant certifications or projects
                            5. Optimize formatting for ATS compatibility
                            """)
                    else:
                        st.success("🎉 **Strong Resume - Minor Tweaks Needed**")
                        with st.expander("Final Optimizations"):
                            st.markdown("""
                            **Polish for Perfection:**
                            1. Fine-tune keyword density
                            2. Add any missing preferred qualifications
                            3. Ensure all achievements are quantified
                            4. Consider adding relevant projects or certifications
                            5. Proofread for any remaining errors
                            """)
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.info("Please check your file format and try again")

# Application entry point
def main():
    checker = ATSChecker()
    checker.show()

if __name__ == "__main__":
    main()

# Export for streamlit
show = ATSChecker().show
