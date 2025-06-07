from transformers import pipeline

# Download and load a model (first time will download weights)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

resume_text = "Your resume text here..."

candidate_labels = ["DevOps Engineer", "Data Scientist", "Product Manager", "Backend Developer", "Frontend Developer"]
result = classifier(resume_text, candidate_labels)
print(result)
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

# --- NEW LOGIC: Only extract skills and suggest courses, no job role logic ---
def extract_skills_and_suggest_courses(resume_text: str, use_gemini: bool = False) -> dict:
    """
    Extracts key skill sets from the resume and provides course links for each skill.
    If use_gemini is True, uses Google Gemini/Vertex AI (placeholder code for hackathon demo).
    Otherwise, uses local extraction logic.
    """
    if use_gemini:
        # --- PLACEHOLDER: Google Gemini/Vertex AI skill extraction ---
        # In a real implementation, you would call the Gemini API here and parse the response.
        # For hackathon demo, we mock the output to match the local logic format.
        # Example (replace with real API call):
        # from vertexai.preview.generative_models import GenerativeModel
        # model = GenerativeModel("gemini-pro")
        # response = model.generate_content(f"Extract skills from this resume: {resume_text}")
        # skills = ...parse response...
        # For now, just return a mock result:
        skills = ["Python", "Docker", "Kubernetes"]  # <-- Replace with parsed Gemini output
        found_skills = sorted(list(set(skills)), key=lambda x: x.lower())
        course_links = {
            skill: {
                "Coursera": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}",
                "Udemy": f"https://www.udemy.com/courses/search/?q={skill.replace(' ', '+')}"
            }
            for skill in found_skills
        }
        return {
            "extracted_skills": found_skills,
            "course_links": course_links,
            "source": "Google Gemini (placeholder)"
        }
    # --- LOCAL LOGIC (as before) ---
    skill_keywords = [
        "Python", "SQL", "Data Analysis", "Power BI", "Statistics", "ETL", "Django", "APIs", "Docker", "CI/CD",
        "Roadmapping", "Stakeholder Management", "Agile", "Communication", "Teamwork", "Kubernetes", "Azure",
        "AWS", "GCP", "Cloud", "DevOps", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Java",
        "C++", "C#", "JavaScript", "React", "Node.js", "Flask", "FastAPI", "Microservices", "REST", "GraphQL",
        "Linux", "Shell Scripting", "Jenkins", "Terraform", "Ansible", "Monitoring", "Prometheus", "Grafana",
        "Product Management", "Business Analysis", "Scrum", "Kanban", "Leadership", "Mentoring", "Testing",
        "Unit Testing", "Integration Testing", "Automation", "CI", "CD", ".NET", "HTML", "CSS", "Vue.js", "Redux",
        "TypeScript", "Responsive Design", "Web Accessibility", "UI/UX", "MongoDB", "Figma", "Sketch", "Adobe XD",
        "Prototyping", "User Research", "Wireframing", "UI Design", "UX Principles", "Accessibility", "Design Systems",
        "Network Security", "Penetration Testing", "Firewalls", "SIEM", "Incident Response", "Ethical Hacking",
        "Risk Assessment", "Cryptography", "Security Policies", "Tableau", "Excel", "Data Visualization", "Data Cleaning", "R"
    ]
    resume_text_lower = resume_text.lower()
    import re
    found_skills = []
    for skill in skill_keywords:
        # Use correct regex for whole word, handle special characters
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text_lower):
            found_skills.append(skill)
    # DEBUG: Print found skills for troubleshooting
    print('DEBUG: Extracted skills:', found_skills)
    # Remove duplicates and sort
    found_skills = sorted(list(set(found_skills)), key=lambda x: x.lower())
    # Generate course links for each skill (Coursera and Udemy)
    course_links = {
        skill: {
            "Coursera": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}",
            "Udemy": f"https://www.udemy.com/courses/search/?q={skill.replace(' ', '+')}"
        }
        for skill in found_skills
    }
    return {
        "extracted_skills": found_skills,
        "course_links": course_links,
        "source": "Local (regex)" if not use_gemini else "Google Gemini (placeholder)"
    }
