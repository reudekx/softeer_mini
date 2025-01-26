from bs4 import BeautifulSoup


def _parse_season_performance(soup: BeautifulSoup) -> dict:
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
            stat_name = item.find("div", class_=lambda x: x and "StatTitle" in x).text
            stat_value = item.find(
                "div", class_=lambda x: x and "StatValue" in x
            ).text.strip()
            stats[group_name][stat_name] = stat_value

    return stats


def _parse_player_traits(soup: BeautifulSoup) -> dict:
    traits = {}

    soup = soup.find("div", class_=lambda x: x and "PlayerTraits" in x)

    trait_labels = soup.find_all("span", class_=lambda x: x and "TraitLabel" in x)

    for label in trait_labels:
        trait_text = label.find("span", class_=lambda x: x and "TraitText" in x).text
        trait_percentage = label.find(
            "span", class_=lambda x: x and "TraitPercentage" in x
        ).text
        traits[trait_text] = trait_percentage

    return traits


def _parse_player_career_main_league(soup: BeautifulSoup) -> dict:
    career = {}

    soup = soup.find("section", class_=lambda x: x and "PlayerCareerMainLeague" in x)

    career["main_league"] = soup.find(
        "h2", class_=lambda x: x and "HeaderText" in x
    ).text

    stat_boxes = soup.find_all("div", class_=lambda x: x and "StatBox" in x)

    for box in stat_boxes:
        title = box.find(class_=lambda x: x and "StatTitle" in x).text
        value = (
            box.find(
                class_=lambda x: x and ("StatValue" in x or "PlayerRatingStyled" in x)
            )
            .find("span")
            .text
        )
        career[title] = value

    return career


def _parse_match_stats(soup: BeautifulSoup) -> list:
    matches = []
    rows = soup.find_all("a", class_=lambda x: x and "PlayerMatchStatsTableRowCSS" in x)

    for row in rows:
        match = {}

        # Parse match info
        left_content = row.find("div", class_=lambda x: x and "LeftContent" in x)

        # League and date
        league_date = left_content.find(
            "div", class_=lambda x: x and "LeagueIconAndDate" in x
        )
        match["league"] = league_date.find("div", {"title": True})["title"]
        match["date"] = league_date.find("p").text

        # Team and score
        team_div = left_content.find(
            "div", class_=lambda x: x and "TeamIconAndName" in x
        )
        match["opponent"] = team_div.text

        result_div = left_content.find("div", class_=lambda x: x and "Result" in x)
        scores = result_div.find_all("span", class_=lambda x: x and "Score" in x)
        match["score"] = f"{scores[0].text.strip()}-{scores[2].text.strip()}"

        # Parse stats
        stats = row.find("div", class_=lambda x: x and "PlayerMatchStatsDataCSS" in x)
        stat_cells = stats.find_all("div", class_=lambda x: x and "DataCell" in x)

        match["minutes"] = stat_cells[0].text.strip()
        match["goals"] = stat_cells[1].text.strip()
        match["assists"] = stat_cells[2].text.strip()
        match["yellow_cards"] = stat_cells[3].text.strip()
        match["red_cards"] = stat_cells[4].text.strip()
        span = stat_cells[5].find("span")
        match["rating"] = span.text.strip() if span else None

        matches.append(match)

    return matches


def parse(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")

    player_stats = {}

    player_stats["season_performance"] = _parse_season_performance(soup)
    player_stats["player_traits"] = _parse_player_traits(soup)
    player_stats["player_career_main_league"] = _parse_player_career_main_league(soup)
    player_stats["match_stats"] = _parse_match_stats(soup)

    return player_stats
