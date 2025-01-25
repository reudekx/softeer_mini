import requests

def fetch_page(url: str) -> str | None:
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def save_html(url: str, save_path: str) -> str | None:
    if html := fetch_page(url):
        with open(save_path, "w") as f:
            f.write(html)
        return html
    return None