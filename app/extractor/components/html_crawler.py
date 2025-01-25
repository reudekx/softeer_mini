import requests

def fetch_page(url: str) -> str | None:
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def save_html(url: str, save_path: str) -> str | None:
    
    try:
        with open(save_path, "r") as f:
            print(f"Reading from {save_path}")
            return f.read()
    except FileNotFoundError:
        pass

    if html := fetch_page(url):
        with open(save_path, "w") as f:
            print(f"Saving to {save_path}")
            f.write(html)
        return html
    return None