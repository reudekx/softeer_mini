from datetime import datetime
from typing import Literal
from .components import html_crawler

from bs4 import BeautifulSoup


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def extract_season_performance(soup: BeautifulSoup) -> dict:
    stats = {}

    soup = soup.find("div", class_=lambda x: x and "SeasonPerformance" in x)

    stat_groups = soup.find_all("h3", class_=lambda x: x and "StatGroupTitle" in x)

    for group in stat_groups:
        group_name = group.text.split("순위")[0]
        stats[group_name] = {}

        stat_items = group.find_next_siblings(
            "div", class_=lambda x: x and "StatItem" in x
        )
        for item in stat_items:
            stat_name = item.find("div", class_= lambda x: x and "StatTitle" in x).text
            stat_value = item.find("div", class_= lambda x: x and "StatValue" in x).text.strip()
            stats[group_name][stat_name] = stat_value

    return stats

def extract_player_traits(soup: BeautifulSoup) -> dict:
    traits = {}

    soup = soup.find("div", class_=lambda x: x and "PlayerTraits" in x)

    trait_labels = soup.find_all("span", class_=lambda x: x and "TraitLabel" in x)

    for label in trait_labels:
        trait_text = label.find("span", class_=lambda x: x and "TraitText" in x).text
        trait_percentage = label.find("span", class_=lambda x: x and "TraitPercentage" in x).text
        traits[trait_text] = trait_percentage

    return traits

def extract_player_career_main_league(soup: BeautifulSoup) -> dict:
    career = {}

    soup = soup.find("section", class_=lambda x: x and "PlayerCareerMainLeague" in x)

    career["main_league"] = soup.find("h2", class_=lambda x: x and "HeaderText" in x).text

    stat_boxes = soup.find_all("div", class_=lambda x: x and "StatBox" in x)

    for box in stat_boxes:
        title = box.find(class_=lambda x: x and "StatTitle" in x).text
        value = box.find(class_=lambda x: x and ("StatValue" in x or "PlayerRatingStyled" in x)).find("span").text
        career[title] = value
            
    return career

def extract(url: str, site: str, name: str, save_path: str) -> bool:
    save_path = save_path.format(
        site=site, name=name, date=datetime.now().strftime("%Y-%m-%d")
    )

    if not (html := html_crawler.save_html(url, save_path)):
        return False

    player_stats = {}

    player_stats["season_performance"] = extract_season_performance(get_soup(html))
    player_stats["player_traits"] = extract_player_traits(get_soup(html))
    player_stats["player_career_main_league"] = extract_player_career_main_league(get_soup(html))

    return player_stats
