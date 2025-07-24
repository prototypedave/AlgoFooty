from utils.logger import logger
from .strings import split_string, split_score
from datetime import datetime

BLOCKED_RESOURCES = {"image", "stylesheet", "font", "media", "other"}
BLOCKED_PATTERNS = ["google-analytics", "ads.", "doubleclick", "tracking"]

async def block_junk(route, request):
    try:
        if request.resource_type in BLOCKED_RESOURCES or any(pattern in request.url for pattern in BLOCKED_PATTERNS):
            await route.abort()
        else:
            await route.continue_()
    except Exception as e:
        logger.error(f"Error in block_junk for {request.url}: {e}")
        await route.continue_()


async def get_header_items(page, caller):
    header_items = await page.locator(".detail__breadcrumbs li").all()
    country, league, round = None, None, None
    if len(header_items) >= 3:
        try:
            country = (await header_items[1].inner_text()).strip().lower()
            league_round = (await header_items[2].inner_text()).strip().lower()
            league, round = split_string(league_round)
            logger.debug(f"{caller} get_header_items: {country}, {league}, {round}")
        except Exception as e:
            logger.debug(f"{caller} get_header_items - {e}")
    return country, league, round


async def get_team_names(page, caller):
    home_team, away_team = None, None
    try:
        home_team = await page.locator(".duelParticipant__home .participant__participantName a").first.text_content()
        home_team = home_team.strip() if home_team else None
        away_team = await page.locator(".duelParticipant__away .participant__participantName a").first.text_content()
        away_team = away_team.strip() if away_team else None
        logger.debug(f"{caller} get_team_names: {home_team}, {away_team}")
    except Exception as e:
        logger.debug(f"{caller} get_team_names - {e}")

    return home_team, away_team

async def get_score(page, caller):
    home_score, away_score = None, None
    try:
        score = await page.locator(".detailScore__wrapper").first.text_content()
        home_score, away_score = split_score(score)
        logger.debug(f"{caller} get_score: {home_score}, {away_score}")
    except Exception as e:
        logger.debug(f"{caller} get_score: {e}")

    return home_score, away_score

async def get_match_time(page, caller):
    match_time = None
    try:
        time_str = await page.locator(".duelParticipant__startTime div").first.text_content()
        match_time = datetime.strptime(time_str.strip(), "%d.%m.%Y %H:%M")
        logger.debug(f"{caller} get_match_time: {match_time}")
    except Exception as e:
        logger.debug(f"{caller} get_match_time - {e}")
    return match_time

async def get_over_odds(page, caller):
    odds = []
    try:
        dup = ""
        odds_row = await page.locator(".ui-table__row").all()
        for row in odds_row:
            odds_locator = await row.locator(".oddsCell__odd").all()
            odd_name = await row.locator(".wcl-oddsCell_djZ95").text_content()               

            if odd_name == "1.5" and dup != "1.5":
                over = await odds_locator[0].text_content()
                under = await odds_locator[1].text_content()
                odds.append({'over_15': over, 'under_15': under})
                dup = odd_name
                continue

            if dup != "2.5" and odd_name == "2.5":
                over = await odds_locator[0].text_content()
                under = await odds_locator[1].text_content()
                odds.append({'over_25': over, 'under_25': under})
                dup = odd_name
                continue

            if dup != "3.5" and odd_name == "3.5":
                over = await odds_locator[0].text_content()
                under = await odds_locator[1].text_content()
                odds.append({'over_35': over, 'under_35': under})
                dup = odd_name
                continue
        logger.debug(f"{caller} get_over_odds: {odds}")
    except Exception as e:
        logger.debug(f"{caller} get_over_odds: {e}")
    return odds

async def get_1x2_odds(page, caller):
    odds = []
    try:
        odds_row = await page.locator(".ui-table__row").all()
        for row in odds_row:
            odds_locator = await row.locator(".oddsCell__odd").all()           
            home = await odds_locator[0].text_content()
            draw = await odds_locator[1].text_content()
            away = await odds_locator[2].text_content()
            odds.append({'home_win': home, 'draw': draw, 'away_win': away})
        logger.debug(f"{caller} get_1x2_odds: {odds}")
    except Exception as e:
        logger.debug(f"{caller} get_1x2_odds  : {e}")
    
    return odds


async def get_btts_odds(page, caller):
    odds = []
    try:
        odds_row = await page.locator(".ui-table__row").all()
        for row in odds_row:
            odds_locator = await row.locator(".oddsCell__odd").all()
            over = await odds_locator[0].text_content()
            under = await odds_locator[1].text_content()
            odds.append({'yes': over, 'no': under})
        logger.debug(f"{caller} get_btts_odds: {odds}")
    except Exception as e:
        logger.debug(f"{caller} get_btts_odds: {e}")
    return odds         


async def get_double_chance_odds(page, caller):
    odds = []
    try: 
        odds_row = await page.locator(".ui-table__row").all()
        for row in odds_row:
            odds_locator = await row.locator(".oddsCell__odd").all()           
            home_draw = await odds_locator[0].text_content()
            home_away = await odds_locator[1].text_content()
            draw_away = await odds_locator[2].text_content()
            odds.append({'1x': home_draw, '12': home_away, 'x2': draw_away})
        logger.debug(f"{caller} get_double_chance_odds: {odds}")
    except Exception as e:
        logger.debug(f"{caller} get_double_chance_odds  : {e}")
    
    return odds