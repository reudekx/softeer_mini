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
    footer = soup.find("div", class_="footer")
    minutes = footer.find("strong").text if footer else None

    # Find all position tables dynamically
    stats = {}
    tables = soup.find_all("table", id=lambda x: x and x.startswith("scout_summary_"))

    for table in tables:
        position = table["id"].replace("scout_summary_", "")
        position_stats = {}

        for row in table.find("tbody").find_all("tr"):
            if "spacer" in row.get("class", []):
                continue

            stat = row.find("th").text.strip()
            per90 = row.find("td", {"data-stat": "per90"}).text.strip()
            percentile = (
                row.find("td", {"data-stat": "percentile"}).find("div").text.strip()
            )

            position_stats[stat] = {"per90": per90, "percentile": percentile}

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

    matches = []
    for row in table.find("tbody").find_all("tr"):
        match = {
            "date": row.find("th", {"data-stat": "date"}).text.strip(),
            "competition": row.find("td", {"data-stat": "round"}).text,
            "venue": row.find("td", {"data-stat": "venue"}).text,
            "result": row.find("td", {"data-stat": "result"}).text,
            "team": row.find("td", {"data-stat": "team"}).text,
            "opponent": row.find("td", {"data-stat": "opponent"}).text,
            "position": row.find("td", {"data-stat": "position"}).text,
            "minutes": row.find("td", {"data-stat": "minutes"}).text,
            "stats": {
                "goals": row.find("td", {"data-stat": "goals"}).text,
                "assists": row.find("td", {"data-stat": "assists"}).text,
                "shots": row.find("td", {"data-stat": "shots"}).text,
                "shots_on_target": row.find(
                    "td", {"data-stat": "shots_on_target"}
                ).text,
                "xg": row.find("td", {"data-stat": "xg"}).text,
                "npxg": row.find("td", {"data-stat": "npxg"}).text,
                "xg_assist": row.find("td", {"data-stat": "xg_assist"}).text,
                "sca": row.find("td", {"data-stat": "sca"}).text,
                "gca": row.find("td", {"data-stat": "gca"}).text,
                "passes_completed": row.find(
                    "td", {"data-stat": "passes_completed"}
                ).text,
                "passes_attempted": row.find("td", {"data-stat": "passes"}).text,
                "progressive_passes": row.find(
                    "td", {"data-stat": "progressive_passes"}
                ).text,
                "carries": row.find("td", {"data-stat": "carries"}).text,
                "progressive_carries": row.find(
                    "td", {"data-stat": "progressive_carries"}
                ).text,
            },
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
