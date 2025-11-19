from datetime import datetime
from flashscore.utils.logger import logger

BLOCKED_RESOURCES = {"image", "stylesheet", "font", "media", "other"}
BLOCKED_PATTERNS = ["google-analytics", "ads.", "doubleclick", "tracking", "tracker"]

def block_junk(route, request):
    try:
        if request.resource_type in BLOCKED_RESOURCES or any(pattern in request.url for pattern in BLOCKED_PATTERNS):
            route.abort()
        else:
            route.continue_()
    except Exception as e:
        logger.debug(f"Error in block_junk for {request.url}: {e}")
        route.continue_()

def get_header_items(page):
    header_items = page.locator(".detail__breadcrumbs li").all()
    country, league, round = None, None, None
    if len(header_items) >= 3:
        try:
            country = (header_items[1].inner_text()).strip().lower()
            league_round = (header_items[2].inner_text()).strip().lower()
            league, round = split_string(league_round)
        except Exception as e:
            logger.debug(f" get_header_items - {e}")
    return country, league, round

import re

def split_score(score_text: str):
    scores = score_text.split("-")
    if len(scores) == 2:
        home_raw, away_raw = scores
        home_score = int(home_raw) if home_raw.isdigit() else None
        away_score = int(away_raw) if away_raw.isdigit() else None

        if home_score is not None and away_score is not None:
            return home_score, away_score

    return None, None

def get_digit_string(text: str) -> str:
    text = re.sub(r"[%()/]", "", text)
    return text.strip()

def split_value(value):
    s = str(value).zfill(2)  

    if len(s) == 2:
        return int(s[0]), int(s[1])
    elif len(s) == 3:
        if s.startswith('10'):
            return 10, int(s[2])
        else:
            return int(s[0]), int(s[1:])
    else:
        raise ValueError(f"Unexpected value format: {value}")


def split_string(input_str: str) -> tuple:
    parts = [p.strip() for p in input_str.split(" - ")]
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 3:
        return parts[0], parts[1] + " - " + parts[2]
    else:
        return parts[0], None
    
def extract_league_gameweek(s: str) -> int:
    s_lower = s.lower()

    if 'qualification' in s_lower or 'group' in s_lower:
        return None

    match = re.search(r'round\s+(\d+)', s_lower)
    if match:
        return int(match.group(1))

    return None

def parse_number(val):
    s = get_digit_string(val)
    if not s:
        return None
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except ValueError:
        return None
    
def get_team_names(page):
    home_team, away_team = None, None
    try:
        home_team = page.locator(".duelParticipant__home .participant__participantName a").first.text_content()
        home_team = home_team.strip() if home_team else None
        away_team = page.locator(".duelParticipant__away .participant__participantName a").first.text_content()
        away_team = away_team.strip() if away_team else None
    except Exception as e:
        logger.debug(f"get_team_names - {e}")

    return home_team, away_team

def get_score(page):
    home_score, away_score = None, None
    try:
        score = page.locator(".detailScore__wrapper").first.text_content()
        home_score, away_score = split_score(score)
    except Exception as e:
        logger.debug(f"get_score: {e}")

    return home_score, away_score

def get_match_time(page):
    match_time = None
    try:
        time_str = page.locator(".duelParticipant__startTime div").first.text_content()
        match_time = datetime.strptime(time_str.strip(), "%d.%m.%Y %H:%M")
    except Exception as e:
        logger.debug(f"get_match_time - {e}")
    return match_time

def get_over_odds(page):
    try:
        rows = page.evaluate("""
        () => {
            return Array.from(document.querySelectorAll(".ui-table__row")).map(row => {
                const oddName = row.querySelector(".wcl-oddsCell_qJ5md")?.textContent?.trim();
                const odds = Array.from(row.querySelectorAll(".oddsCell__odd")).map(e => e.textContent?.trim());
                return { oddName, odds };
            });
        }
        """)

        odds = []
        seen = set()
        for row in rows:
            if row["oddName"] in ("1.5", "2.5", "3.5") and row["oddName"] not in seen:
                odds.append({
                    f"over_{row['oddName'].replace('.','')}": row["odds"][0],
                    f"under_{row['oddName'].replace('.','')}": row["odds"][1]
                })
                seen.add(row["oddName"])
        return odds
    except Exception as e:
        logger.debug(f"get_over_odds: {e}")
        return []

def get_1x2_odds(page):
    try:
        rows = page.evaluate("""
        () => Array.from(document.querySelectorAll(".ui-table__row")).map(row => {
            const odds = Array.from(row.querySelectorAll(".oddsCell__odd")).map(e => e.textContent?.trim());
            return { home_win: odds[0], draw: odds[1], away_win: odds[2] };
        })
        """)
        return rows
    except Exception as e:
        logger.debug(f"get_1x2_odds: {e}")
        return []

def get_btts_odds(page):
    try:
        rows = page.evaluate("""
        () => Array.from(document.querySelectorAll(".ui-table__row")).map(row => {
            const odds = Array.from(row.querySelectorAll(".oddsCell__odd")).map(e => e.textContent?.trim());
            return { yes: odds[0], no: odds[1] };
        })
        """)
        return rows
    except Exception as e:
        logger.debug(f"get_btts_odds: {e}")
        return []
        
def get_double_chance_odds(page):
    try:
        rows = page.evaluate("""
        () => Array.from(document.querySelectorAll(".ui-table__row")).map(row => {
            const odds = Array.from(row.querySelectorAll(".oddsCell__odd")).map(e => e.textContent?.trim());
            return { "1x": odds[0], "12": odds[1], "x2": odds[2] };
        })
        """)
        return rows
    except Exception as e:
        logger.debug(f"get_double_chance_odds: {e}")
        return []
