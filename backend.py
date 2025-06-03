import io
import json
import os
from typing import Dict, List

# Placeholder: Extract text from uploaded resume (PDF or text)
def extract_resume_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_file)
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            return text
        except Exception:
            return "[Error reading PDF]"
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

# Placeholder: Call Gemini API to extract skills, experience, etc.
def analyze_resume_with_gemini(resume_text: str) -> Dict:
    """
    Calls Gemini API via Vertex AI to extract skills, soft skills, domains, experience level, and achievements from resume text.
    Requires google-cloud-aiplatform and proper authentication.
    """
    try:
        import vertexai
        from vertexai.preview.generative_models import GenerativeModel, Part
        # Initialize Vertex AI with your project and location
        vertexai.init(project="pelagic-cat-461817-q8", location="us-central1")
        model = GenerativeModel("gemini-1.5-pro")
        prompt = (
            "You are an AI Career Analyst. From the following resume, extract a list of technical skills, soft skills, "
            "domains of expertise, experience level, and notable achievements. Format the result in structured JSON.\n\nResume:\n" + resume_text
        )
        response = model.generate_content(prompt)
        import json as _json
        # Try to extract JSON from the response
        try:
            import re
            match = re.search(r'```json\\n(.*?)```', response.text, re.DOTALL)
            if match:
                result_json = match.group(1)
            else:
                result_json = response.text
            result = _json.loads(result_json)
            return result
        except Exception:
            return {"raw_response": response.text}
    except Exception as e:
        # Fallback to keyword-based extraction if Gemini API fails
        # Simple keyword-based skill extraction as a placeholder
        common_skills = [
            "Python", "SQL", "Data Analysis", "Power BI", "Statistics", "ETL",
            "Django", "APIs", "Docker", "CI/CD", "Roadmapping", "Stakeholder Management",
            "Agile", "Communication", "Teamwork"
        ]
        found_skills = [skill for skill in common_skills if skill.lower() in resume_text.lower()]
        # Simple soft skills and domains extraction
        soft_skills = [s for s in ["Communication", "Teamwork"] if s.lower() in resume_text.lower()]
        domains = [d for d in ["Data Science", "Backend Development", "Product Management"] if d.lower() in resume_text.lower()]
        # Experience level (very basic)
        if "senior" in resume_text.lower():
            experience_level = "Senior"
        elif "junior" in resume_text.lower():
            experience_level = "Junior"
        else:
            experience_level = "Mid-level"
        # Achievements (mocked)
        achievements = []
        if "improved" in resume_text.lower():
            achievements.append("Improved process or system")
        return {
            "skills": found_skills,
            "soft_skills": soft_skills,
            "domains": domains,
            "experience_level": experience_level,
            "achievements": achievements,
            "error": str(e)
        }

# Placeholder: Match extracted skills to job roles and suggest learning paths
def match_roles_and_suggest_learning(extracted: Dict) -> Dict:
    # Load job roles dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "job_roles.json")
    with open(dataset_path, "r") as f:
        roles = json.load(f)
    user_skills = set(extracted.get("skills", []))
    best_match = None
    best_score = -1
    missing_skills = []
    for role in roles:
        required_skills = set(role["skills"])
        match_count = len(user_skills & required_skills)
        score = int(100 * match_count / len(required_skills))
        if score > best_score:
            best_score = score
            best_match = role
            missing_skills = list(required_skills - user_skills)
    # Mock learning suggestions
    learning_suggestions = [
        "https://www.coursera.org/learn/data-visualization",
        "https://www.youtube.com/watch?v=xyz"
    ]
    return {
        "best_matched_role": best_match["role"] if best_match else None,
        "match_score": best_score,
        "missing_skills": missing_skills,
        "learning_suggestions": learning_suggestions
    }
