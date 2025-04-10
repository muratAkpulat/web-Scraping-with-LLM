import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print("✅ HTML fetched successfully!")
        return response.text
    except requests.RequestException as e:
        print(f"❌ Error occurred while fetching the page: {e}")
        return None

def extract_clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove unwanted elements (scripts, styles, navbars, etc.)
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    
    # Get the visible text
    text = soup.get_text(separator="\n")
    
    # Clean up extra whitespace
    lines = [line.strip() for line in text.splitlines()]
    clean_lines = [line for line in lines if line]  # remove empty lines
    cleaned_text = "\n".join(clean_lines)
    
    return cleaned_text


