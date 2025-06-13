import os
import re
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Make sure OPENROUTER_API_KEY is in your .env file.")

def analyze_resume(resume_text: str) -> dict:
    prompt = build_prompt(resume_text)

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://loclhost",
            "X-Title": "Resume Analyzer",
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )

    if response.status_code != 200:
        raise Exception(f"LLM API error: {response.status_code} - {response.text}")

    content = response.json()['choices'][0]['message']['content']
    content_clean = re.sub(r"^```(?:json)?\n([\s\S]+?)\n```$", r"\1", content.strip(), flags=re.MULTILINE)

    try:
        return json.loads(content_clean)
    except Exception as e:
        raise Exception(f"Failed to parse LLM output as JSON. Raw response:\n{response.text}\n\nError: {e}")


def build_prompt(resume_text: str) -> str:
    return f"""
You are a resume analysis assistant.

Analyze the following resume text and return a JSON with the following fields:
- sections_detected: list of strings
- missing_sections: list of strings
- well_written_sections: list of strings (and give reasons as short strings)
- llm_evaluation: integer between 0 and 10
- skills_sentiment_summary: short string
- improvement_suggestions: list of short strings
- resume_data: additionally, extract the resume into a nested JSON object with structured data using this (strict) schema:
  - personal_info: name, email, mobile, location
  - experience: only title, company, duration, details
  - education: only institution, degree, year
  - skills: list of technical and soft skills
  - projects: only project titles and descriptions

Resume text:
\"\"\"
{resume_text}
\"\"\"

Respond ONLY with a JSON object matching the above structure. Be slightly more critical in your analysis.
    """.strip()
