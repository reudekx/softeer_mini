from bs4 import BeautifulSoup


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def get_player_stats(soup: BeautifulSoup) -> dict:


    soup.find_all(class_=lambda x: x and 'text' in x)