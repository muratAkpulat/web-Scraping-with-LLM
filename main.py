from scraper import fetch_html, extract_clean_text
from llm import summarize_with_llm
import json
import os

def extract_json_block(llm_output):
    try:
        start = llm_output.index('{')
        end = llm_output.rindex('}') + 1
        json_text = llm_output[start:end]
        return json.loads(json_text)
    except Exception as e:
        print(f"[ERROR] Failed to extract JSON block: {e}")
        return None

def save_json(data, filename):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ JSON result saved to {path}")

def main():
    url = "https://www.milliyet.com.tr"
    html = fetch_html(url)
    
    if html:
        clean_text = extract_clean_text(html)
        llm_output = summarize_with_llm(clean_text[:10000])
        
        print("\n🔎 Gemini Result:\n")
        print(llm_output[:10000])  # Preview first 1000 chars

        parsed_json = extract_json_block(llm_output)
        if parsed_json:
            save_json(parsed_json, "ml_summary.json")
        else:
            print("❌ Could not extract structured JSON.")
    else:
        print("❌ Failed to fetch HTML.")

if __name__ == "__main__":
    main()
