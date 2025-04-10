import gradio as gr
from scraper import fetch_html, extract_clean_text
from llm import summarize_with_llm
import json

def summarize_url_local(url):
    html = fetch_html(url)
    if not html:
        return "❌ Failed to fetch HTML.", "", ""

    clean_text = extract_clean_text(html)
    llm_output = summarize_with_llm(clean_text[:5000])

    try:
        start = llm_output.index("{")
        end = llm_output.rindex("}") + 1
        result = json.loads(llm_output[start:end])
        return result["summary"], result["page_type"], result["language"]
    except Exception as e:
        return f"❌ Error parsing LLM response: {e}", "", ""

# Gradio Interface
gr.Interface(
    fn=summarize_url_local,
    inputs=gr.Textbox(label="Enter a URL"),
    outputs=[
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Page Type"),
        gr.Textbox(label="Language")
    ],
    title="🌐 Gemini Web Summarizer (Local)",
    description="Fetches and summarizes the content of a webpage using Gemini LLM (local functions)."
).launch()
