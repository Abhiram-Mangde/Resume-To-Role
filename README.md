# Resume-To-Role – Smart Resume Analyzer & Career Matcher

🚀 **What it does:**

Upload your resume → Gemini API + Vertex AI analyzes your skills → suggests best-fit career roles, highlights skill gaps, and generates personalized learning paths using public data (e.g., Coursera, YouTube).

🔧 **Tools:**

- **Gemini API** → Understanding resume & job descriptions
- **Vertex AI Embeddings** → Similarity scoring
- **Streamlit** → Upload + interactive UI
- **Optional:** Integrate with LinkedIn job API or scrape job data for real-world matching

💥 **Why it's impactful:**

- Every job seeker can benefit
- High relevance, easy deployment
- Shows real use of embeddings, LLMs, and RAG

---

# Documentation: Resume-To-Role – Smart Resume Analyzer & Career Matcher

## Step 1: Define the Workflow & Architecture

### 🎯 What the app will do:
1. User uploads resume (PDF/text)
2. Gemini API reads and extracts skills, experience, domain, etc.
3. Gemini matches these against a set of curated job roles
4. Calculates matching score + highlights missing skills
5. Suggests upskilling paths using real links (Coursera/YouTube)
6. All done in a clean Streamlit UI

---

## Step 2: Prepare the Dataset

We'll need:
- A list of job roles (e.g., Data Analyst, Backend Developer, Product Manager)
- For each role:
  - Skills required
  - Typical responsibilities (to help Gemini understand better)

➡️ Starter JSON/CSV for these roles will be created.

---

## Step 3: Build the Resume Skill Extractor

### 🔧 Tools:
- Gemini API (via Vertex AI or Generative AI Studio)

**Prompt Example:**
> "You are an AI Career Analyst. From the following resume, extract a list of technical skills, soft skills, domains of expertise, experience level, and notable achievements. Format the result in structured JSON."

Resume:
[Paste user’s resume content here]

We'll use gemini-pro or gemini-1.5-pro for this in Python or Streamlit.

---

## Step 4: Role Matching & Gap Analysis

Match extracted skills to roles using:
- Vector Embeddings (Vertex AI Embeddings API) to find best-fit roles
- Calculate % match and identify missing skills

**Example output:**
```json
{
  "best_matched_role": "Data Analyst",
  "match_score": 78,
  "missing_skills": ["Power BI", "Statistics", "ETL"],
  "learning_suggestions": [
    "https://www.coursera.org/learn/data-visualization",
    "https://www.youtube.com/watch?v=xyz"
  ]
}
```

---

## Step 5: Build the Streamlit UI

Your app will have 3 main parts:
1. Upload Resume (PDF or text)
2. View Analysis (Skills, roles, match %, gaps)
3. Learning Suggestions (auto-linked)

**Bonus:**
- Save results as downloadable PDF
