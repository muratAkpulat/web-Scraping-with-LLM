from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import fetch_html, extract_clean_text
from llm import summarize_with_llm
import json

app = FastAPI()

class SummarizeRequest(BaseModel):
    url: str

class SummarizeResponse(BaseModel):
    summary: str
    page_type: str
    language: str

@app.post("/summarize", response_model=SummarizeResponse)
def summarize_url(request: SummarizeRequest):
    html = fetch_html(request.url)
    if not html:
        raise HTTPException(status_code=400, detail="Failed to fetch HTML.")

    clean_text = extract_clean_text(html)
    llm_output = summarize_with_llm(clean_text[:5000])

    try:
        start = llm_output.index('{')
        end = llm_output.rindex('}') + 1
        json_text = llm_output[start:end]
        result = json.loads(json_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JSON: {e}")
