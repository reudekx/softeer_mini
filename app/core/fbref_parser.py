from bs4 import BeautifulSoup

def _parse_stats(soup: BeautifulSoup) -> dict:

    stats_div = soup.find("div", class_="stats_pullout")
    if not stats_div:
        return None

    header = stats_div.find("div")
    season = header.find("strong").text if header and header.find("strong") else None
    competitions = [p.text for p in header.find_all("p")] if header else []

    stats = {}
    for div in stats_div.find_all("div", class_=lambda x: x and x.startswith("p")):
        for stat_div in div.find_all("div", recursive=False):
            stat_name = stat_div.find("strong")
            if not stat_name:
                continue

            values = [p.text for p in stat_div.find_all("p")]
            stats[stat_name.text] = values

    return {"season": season, "competitions": competitions, "stats": stats}

def _parse_scouting_report(soup: BeautifulSoup) -> dict:
    def get_text(element):
        return element.text.strip() if element else None

    # Parse footer minutes
    footer = soup.find("div", class_="footer")
    strong_element = footer.find("strong") if footer else None
    minutes = get_text(strong_element)

    # Find all position tables dynamically
    stats = {}
    tables = soup.find_all("table", id=lambda x: x and x.startswith("scout_summary_"))
    if not tables:
        return {"minutes_played": minutes, "stats": stats}

    for table in tables:
        position = table["id"].replace("scout_summary_", "")
        position_stats = {}

        tbody = table.find("tbody")
        if not tbody:
            continue

        for row in tbody.find_all("tr"):
            if "spacer" in row.get("class", []):
                continue

            th_element = row.find("th")
            per90_element = row.find("td", {"data-stat": "per90"})
            percentile_element = row.find("td", {"data-stat": "percentile"})
            
            if not all([th_element, per90_element, percentile_element]):
                continue

            stat = get_text(th_element)
            per90 = get_text(per90_element)
            
            # percentile is nested in a div
            percentile_div = percentile_element.find("div")
            percentile = get_text(percentile_div) if percentile_div else None

            if stat:  # Only add if we have a valid stat name
                position_stats[stat] = {
                    "per90": per90,
                    "percentile": percentile
                }

        if position_stats:  # Only add if we have any stats for this position
            stats[position] = position_stats

    return {"minutes_played": minutes, "stats": stats}


def _parse_similar_players(soup: BeautifulSoup) -> dict:
    similar_players = {}
    similar_tables = soup.find_all("table", id=lambda x: x and x.startswith("similar_"))

    for table in similar_tables:
        position = table["id"].replace("similar_", "")
        players = []

        for row in table.find("tbody").find_all("tr"):
            cells = {
                "player": row.find("td", {"data-stat": "player"}),
                "nation": row.find("td", {"data-stat": "nationality"}),
                "team": row.find("td", {"data-stat": "team"}),
            }

            if not all(cells.values()):
                continue

            links = {
                "player": cells["player"].find("a"),
                "nation": cells["nation"].find("a"),
                "team": cells["team"].find("a"),
            }

            if not all(links.values()):
                continue

            player_id = links["player"]["href"].split("/")[-1].replace("-Stats", "")
            nation_code = (
                links["nation"]
                .find("span", class_="f-i")["class"][1]
                .split("-")[-1]
                .upper()
            )

            players.append(
                {
                    "name": links["player"].text,
                    "id": player_id,
                    "nation": {
                        "name": links["nation"].text.strip()[-3:],
                        "code": nation_code,
                    },
                    "team": links["team"].text,
                }
            )

        if players:
            similar_players[position] = players

    return similar_players


def _parse_last_matches(soup: BeautifulSoup) -> list:
    table = soup.find("table", id="last_5_matchlogs")
    if not table:
        return []

    def get_text(element):
        return element.text.strip() if element else None

    matches = []
    for row in table.find("tbody").find_all("tr"):
        match = {
            "date": get_text(row.find("th", {"data-stat": "date"})),
            "competition": get_text(row.find("td", {"data-stat": "round"})),
            "venue": get_text(row.find("td", {"data-stat": "venue"})),
            "result": get_text(row.find("td", {"data-stat": "result"})),
            "team": get_text(row.find("td", {"data-stat": "team"})),
            "opponent": get_text(row.find("td", {"data-stat": "opponent"})),
            "position": get_text(row.find("td", {"data-stat": "position"})),
            "minutes": get_text(row.find("td", {"data-stat": "minutes"})),
            "stats": {
                "goals": get_text(row.find("td", {"data-stat": "goals"})),
                "assists": get_text(row.find("td", {"data-stat": "assists"})),
                "shots": get_text(row.find("td", {"data-stat": "shots"})),
                "shots_on_target": get_text(row.find("td", {"data-stat": "shots_on_target"})),
                "xg": get_text(row.find("td", {"data-stat": "xg"})),
                "npxg": get_text(row.find("td", {"data-stat": "npxg"})),
                "xg_assist": get_text(row.find("td", {"data-stat": "xg_assist"})),
                "sca": get_text(row.find("td", {"data-stat": "sca"})),
                "gca": get_text(row.find("td", {"data-stat": "gca"})),
                "passes_completed": get_text(row.find("td", {"data-stat": "passes_completed"})),
                "passes_attempted": get_text(row.find("td", {"data-stat": "passes"})),
                "progressive_passes": get_text(row.find("td", {"data-stat": "progressive_passes"})),
                "carries": get_text(row.find("td", {"data-stat": "carries"})),
                "progressive_carries": get_text(row.find("td", {"data-stat": "progressive_carries"}))
            }
        }
        matches.append(match)

    return matches


def parse(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")

    player_stats = {}

    player_stats["stats"] = _parse_stats(soup)
    player_stats["scouting_report"] = _parse_scouting_report(soup)
    player_stats["similar_players"] = _parse_similar_players(soup)
    player_stats["last_matches"] = _parse_last_matches(soup)

    return player_stats
