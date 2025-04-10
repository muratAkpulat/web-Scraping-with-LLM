import gradio as gr
import requests

def summarize_url_via_api(url):
    api_url = "http://localhost:8000/summarize"
    try:
        response = requests.post(api_url, json={"url": url})
        if response.status_code == 200:
            data = response.json()
            return data["summary"], data["page_type"], data["language"]
        else:
            return f"❌ API Error {response.status_code}: {response.json()['detail']}", "", ""
    except Exception as e:
        return f"❌ Request failed: {e}", "", ""

# Gradio Interface
gr.Interface(
    fn=summarize_url_via_api,
    inputs=gr.Textbox(label="Enter a URL"),
    outputs=[
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Page Type"),
        gr.Textbox(label="Language")
    ],
    title="🌐 Gemini Web Summarizer (API)",
    description="Sends request to FastAPI backend and displays the Gemini LLM summary."
).launch()
