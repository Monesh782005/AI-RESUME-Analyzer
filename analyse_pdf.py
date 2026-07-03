import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def analyse_resume_gemini(resume_text, job_description):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Compare the following resume with the given job description.

Resume
------
{resume_text}

Job Description
---------------
{job_description}

Provide:

1. ATS Score (0-100)
2. Matching Skills
3. Missing Skills
4. Strengths
5. Weaknesses
6. Suggestions
7. Final Recommendation

Return the response in proper markdown.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text