from datetime import datetime
from .components import html_crawler

from bs4 import BeautifulSoup

def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def get_player_stats(soup: BeautifulSoup) -> dict:
    stats = {}

    soup.find_all(class_=lambda x: x and 'text' in x)

def extract(url: str, save_path: str) -> bool:
    save_path = save_path.format(site="fotmob", name="heung-min-son", date=datetime.now().strftime("%Y-%m-%d"))
    return html_crawler.save_html(url, save_path)
        