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
        vertexai.init(project="resumetorole", location="us-central1")
        model = GenerativeModel("gemini-pro")
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
    except Exception:
        # Fallback to local Hugging Face zero-shot-classification (no token required)
        try:
            from transformers import pipeline
            candidate_labels = [
                "DevOps Engineer", "Data Scientist", "Product Manager", "Backend Developer", "Frontend Developer",
                "Cloud Engineer", "QA Engineer", "Full Stack Developer"
            ]
            classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            result = classifier(resume_text, candidate_labels)
            # Get the best matching role and scores
            best_role = result['labels'][0] if result['labels'] else None
            scores = dict(zip(result['labels'], result['scores']))
            return {
                "best_matched_role": best_role,
                "role_scores": scores
            }
        except Exception:
            # If local model fails, fallback to enhanced keyword-based extraction
            skill_keywords = [
                "Python", "SQL", "Data Analysis", "Power BI", "Statistics", "ETL", "Django", "APIs", "Docker", "CI/CD",
                "Roadmapping", "Stakeholder Management", "Agile", "Communication", "Teamwork", "Kubernetes", "Azure",
                "AWS", "GCP", "Cloud", "DevOps", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Java",
                "C++", "C#", "JavaScript", "React", "Node.js", "Flask", "FastAPI", "Microservices", "REST", "GraphQL",
                "Linux", "Shell Scripting", "Jenkins", "Terraform", "Ansible", "Monitoring", "Prometheus", "Grafana",
                "Product Management", "Business Analysis", "Scrum", "Kanban", "Leadership", "Mentoring", "Testing",
                "Unit Testing", "Integration Testing", "Automation", "CI", "CD"
            ]
            domain_keywords = [
                "Data Science", "Backend Development", "Frontend Development", "Product Management", "Cloud Engineering",
                "DevOps", "AI/ML", "Business Analysis", "Project Management", "QA", "Testing", "Full Stack", "Security"
            ]
            role_keywords = {
                "Data Scientist": ["machine learning", "data analysis", "python", "statistics", "deep learning", "pandas", "scikit-learn"],
                "Backend Developer": ["django", "flask", "node.js", "api", "microservices", "sql", "java", "c#", "fastapi"],
                "DevOps Engineer": ["ci/cd", "jenkins", "docker", "kubernetes", "terraform", "ansible", "cloud", "azure", "aws", "gcp", "devops"],
                "Cloud Engineer": ["azure", "aws", "gcp", "cloud", "vm", "app services", "functions", "infrastructure"],
                "Product Manager": ["roadmapping", "stakeholder", "agile", "scrum", "kanban", "product", "vision", "requirements", "manager"],
                "QA Engineer": ["testing", "automation", "unit testing", "integration testing", "selenium", "qa", "test cases"],
                "Frontend Developer": ["react", "javascript", "css", "html", "frontend", "ui", "ux", "typescript"],
                "Full Stack Developer": ["frontend", "backend", "full stack", "react", "django", "node.js", "api", "sql"]
            }
            found_skills = [skill for skill in skill_keywords if skill.lower() in resume_text.lower()]
            found_domains = [d for d in domain_keywords if d.lower() in resume_text.lower()]
            found_roles = []
            for role, keywords in role_keywords.items():
                for kw in keywords:
                    if kw in resume_text.lower():
                        found_roles.append(role)
                        break
            # Simple soft skills extraction
            soft_skills = [s for s in ["Communication", "Teamwork", "Leadership", "Mentoring"] if s.lower() in resume_text.lower()]
            # Experience level
            if "senior" in resume_text.lower():
                experience_level = "Senior"
            elif "junior" in resume_text.lower():
                experience_level = "Junior"
            elif "lead" in resume_text.lower() or "manager" in resume_text.lower():
                experience_level = "Lead/Manager"
            else:
                experience_level = "Mid-level"
            # Achievements (mocked)
            achievements = []
            if "improved" in resume_text.lower():
                achievements.append("Improved process or system")
            if "patent" in resume_text.lower():
                achievements.append("Patent holder")
            if "award" in resume_text.lower():
                achievements.append("Award winner")
            return {
                "skills": found_skills,
                "soft_skills": soft_skills,
                "domains": found_domains,
                "possible_roles": list(set(found_roles)),
                "experience_level": experience_level,
                "achievements": achievements
            }

# Placeholder: Match extracted skills to job roles and suggest learning paths
def match_roles_and_suggest_learning(extracted: Dict) -> Dict:
    # Use the provided roles and their mandatory skills
    roles = [
        {
            "role": "Data Analyst",
            "skills": ["Python", "SQL", "Excel", "Power BI", "Tableau", "Data Visualization", "Statistics", "ETL", "Data Cleaning", "R"]
        },
        {
            "role": "Backend Developer",
            "skills": ["C#", "Java", "Python", ".NET", "Node.js", "REST API", "SQL", "MongoDB", "Docker", "Microservices"]
        },
        {
            "role": "Frontend Developer",
            "skills": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Redux", "TypeScript", "Responsive Design", "Web Accessibility", "UI/UX"]
        },
        {
            "role": "DevOps Engineer",
            "skills": ["CI/CD", "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "Git", "Linux", "Monitoring", "Cloud"]
        },
        {
            "role": "Data Scientist",
            "skills": ["Python", "R", "Machine Learning", "Deep Learning", "Pandas", "Numpy", "Scikit-learn", "TensorFlow", "Keras", "Data Visualization"]
        },
        {
            "role": "AI/ML Engineer",
            "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "Model Deployment", "MLOps", "Data Engineering", "Computer Vision", "NLP"]
        },
        {
            "role": "Cloud Engineer",
            "skills": ["AWS", "Azure", "Google Cloud", "Terraform", "Kubernetes", "Docker", "Linux", "CI/CD", "Cloud Security", "Networking"]
        },
        {
            "role": "Product Manager",
            "skills": ["Product Strategy", "Agile", "Scrum", "Market Research", "Wireframing", "Stakeholder Management", "Data Analysis", "User Stories", "Prototyping", "Roadmapping"]
        },
        {
            "role": "UI/UX Designer",
            "skills": ["Figma", "Sketch", "Adobe XD", "Prototyping", "User Research", "Wireframing", "UI Design", "UX Principles", "Accessibility", "Design Systems"]
        },
        {
            "role": "Cybersecurity Analyst",
            "skills": ["Network Security", "Penetration Testing", "Firewalls", "SIEM", "Incident Response", "Ethical Hacking", "Linux", "Risk Assessment", "Cryptography", "Security Policies"]
        }
    ]
    # Normalize user skills: lowercase, strip whitespace, remove empty
    user_skills = set([s.lower().strip() for s in extracted.get("skills", []) if s and isinstance(s, str)])
    # If the resume has a domain that matches a role, use that role
    domain_to_role = {r["role"].lower(): r["role"] for r in roles}
    for domain in extracted.get("domains", []):
        if isinstance(domain, str) and domain.lower().strip() in domain_to_role:
            return {
                "best_matched_role": domain_to_role[domain.lower().strip()],
                "match_score": 100,
                "missing_skills": [],
                "learning_suggestions": []
            }
    # DevOps prioritization logic
    devops_role = next((r for r in roles if r["role"] == "DevOps Engineer"), None)
    devops_skills = set([s.lower().strip() for s in devops_role["skills"]])
    devops_matched = set()
    for skill in devops_skills:
        for user_skill in user_skills:
            if skill and user_skill and (skill in user_skill or user_skill in skill):
                devops_matched.add(skill)
    if len(devops_matched) >= 4:
        missing_skills = list(devops_skills - devops_matched)
        learning_suggestions = [
            f"https://www.coursera.org/search?query={skill.replace(' ', '+')}" for skill in missing_skills[:3]
        ]
        return {
            "best_matched_role": "DevOps Engineer",
            "match_score": int(100 * len(devops_matched) / len(devops_skills)),
            "missing_skills": missing_skills,
            "learning_suggestions": learning_suggestions
        }
    # Otherwise, score each role by number of matched skills (substring match, normalized)
    best_match = None
    best_score = -1
    best_count = -1
    missing_skills = []
    for role in roles:
        required_skills = set([s.lower().strip() for s in role["skills"]])
        matched = set()
        for skill in required_skills:
            for user_skill in user_skills:
                if skill and user_skill and (skill in user_skill or user_skill in skill):
                    matched.add(skill)
        match_count = len(matched)
        score = int(100 * match_count / len(required_skills))
        if score > best_score or (score == best_score and match_count > best_count):
            best_score = score
            best_count = match_count
            best_match = role
            missing_skills = list(required_skills - matched)
    learning_suggestions = [
        f"https://www.coursera.org/search?query={skill.replace(' ', '+')}" for skill in missing_skills[:3]
    ]
    return {
        "best_matched_role": best_match["role"] if best_match else None,
        "match_score": best_score,
        "missing_skills": missing_skills,
        "learning_suggestions": learning_suggestions
    }
