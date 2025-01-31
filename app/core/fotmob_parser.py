from bs4 import BeautifulSoup

from bs4 import BeautifulSoup
import re

def _parse_career_history(soup: BeautifulSoup) -> dict:
    career_data = {}
    
    # Find all career phase sections (고위급 경력, 청년 경력, 국가대표 팀)
    career_phases = soup.find_all('tbody', class_='css-1j17bv1-CareerPhaseTbody')
    
    for phase in career_phases:
        # Get phase title from the header
        phase_header = phase.find('h4', class_='css-1pht4b8-CareerPhaseH4')
        if not phase_header:
            continue
            
        phase_name = phase_header.text.strip()
        career_data[phase_name] = []
        
        # Find all team rows in this phase
        team_rows = phase.find_all('tr', class_='css-1k09b8v-TeamAndSeasonsCSS')
        
        for row in team_rows:
            team_data = {}
            
            # Get team info
            team_cell = row.find('div', class_='css-1gjc1yn-TeamCSS')
            if team_cell:
                # Team name
                team_name_elem = team_cell.find('span', class_='css-1jnt5s3-TeamName')
                if team_name_elem:
                    team_name = team_name_elem.text.split('(')[0].strip()  # Remove any (임대) suffix
                    team_data['team'] = team_name
                
                # Date range
                date_elem = team_cell.find('span', class_='css-hrqiwh-DateCSS')
                if date_elem:
                    team_data['period'] = date_elem.text.strip()
                
                # Transfer status (임대, 임대 복귀 등)
                transfer_suffix = team_cell.find('span', class_='css-xzamas-TransferSuffix')
                if transfer_suffix and transfer_suffix.text.strip():
                    team_data['status'] = transfer_suffix.text.strip(' ()')
            
            # Get stats
            stats_cells = row.find_all('div', class_='css-17xcm4a-StatCell')
            if stats_cells:
                # Assuming the order is: appearances, goals
                for i, stat in enumerate(stats_cells):
                    stat_value = stat.find('span')
                    if stat_value:
                        if i == 1:  # Appearances
                            team_data['appearances'] = int(stat_value.text)
                        elif i == 2:  # Goals
                            team_data['goals'] = int(stat_value.text)
            
            if team_data:
                career_data[phase_name].append(team_data)
    
    return career_data

def _parse_season_performance(soup: BeautifulSoup) -> dict:
    stats = {}
    
    performance_div = soup.find("div", class_=lambda x: x and "SeasonPerformance" in x)
    if not performance_div:
        return stats

    stat_groups = performance_div.find_all("h3", class_=lambda x: x and "StatGroupTitle" in x)
    if not stat_groups:
        return stats

    def get_text(element):
        return element.text.strip() if element else None

    for group in stat_groups:
        group_name = get_text(group).split("순위")[0] if get_text(group) else "Unknown"
        stats[group_name] = {}

        stat_items = group.find_next_siblings(
            "div", class_=lambda x: x and "StatItem" in x
        )
        
        if not stat_items:
            continue

        for item in stat_items:
            stat_title_div = item.find("div", class_=lambda x: x and "StatTitle" in x)
            stat_value_div = item.find("div", class_=lambda x: x and "StatValue" in x)
            
            stat_name = get_text(stat_title_div) if stat_title_div else "Unknown"
            stat_value = get_text(stat_value_div) if stat_value_div else None
            
            stats[group_name][stat_name] = stat_value

    return stats


def _parse_player_traits(soup: BeautifulSoup) -> dict:
    traits = {}

    def get_text(element):
        return element.text.strip() if element else None

    # Find traits container
    traits_container = soup.find("div", class_=lambda x: x and "PlayerTraits" in x)
    if not traits_container:
        return traits

    # Find all trait labels
    trait_labels = traits_container.find_all("span", class_=lambda x: x and "TraitLabel" in x)
    if not trait_labels:
        return traits

    for label in trait_labels:
        # Find trait text and percentage spans
        trait_text_span = label.find("span", class_=lambda x: x and "TraitText" in x)
        trait_percentage_span = label.find("span", class_=lambda x: x and "TraitPercentage" in x)

        # Get text values with None check
        trait_text = get_text(trait_text_span)
        trait_percentage = get_text(trait_percentage_span)

        # Only add if both values are present
        if trait_text and trait_percentage:
            traits[trait_text] = trait_percentage

    return traits


def _parse_player_career_main_league(soup: BeautifulSoup) -> dict:
    career = {}

    # Find the career section
    career_section = soup.find("section", class_=lambda x: x and "PlayerCareerMainLeague" in x)
    if not career_section:
        return career

    def get_text(element):
        return element.text.strip() if element else None

    # Find and parse header
    header = career_section.find("h2", class_=lambda x: x and "HeaderText" in x)
    career["main_league"] = get_text(header)

    # Find all stat boxes
    stat_boxes = career_section.find_all("div", class_=lambda x: x and "StatBox" in x)
    if not stat_boxes:
        return career

    for box in stat_boxes:
        # Find title element
        title_element = box.find(class_=lambda x: x and "StatTitle" in x)
        if not title_element:
            continue
        
        # Find value element (which might be in StatValue or PlayerRatingStyled)
        value_element = box.find(
            class_=lambda x: x and ("StatValue" in x or "PlayerRatingStyled" in x)
        )
        if not value_element:
            continue

        # Find span within value element
        span_element = value_element.find("span")
        if not span_element:
            continue

        title = get_text(title_element)
        value = get_text(span_element)

        if title and value:  # Only add if both title and value are present
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
    player_stats["career_history"] = _parse_career_history(soup)

    return player_stats
