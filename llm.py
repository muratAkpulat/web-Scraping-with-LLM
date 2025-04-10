import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use correct model name
model = genai.GenerativeModel("models/gemini-2.5-pro-exp-03-25")


def summarize_with_llm(text):
    prompt = f"""
    Analyze the following website content and return:
    1. A short summary
    2. The type of the page (about/contact/services/other)
    3. A JSON output with the fields:
        {{
            "summary": "...",
            "page_type": "...",
            "language": "..."
        }}
    \n\nContent:\n{text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[LLM ERROR] {e}"
