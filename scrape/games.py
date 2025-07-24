from .events import get_links
from .h2h import get_h2h
from .odds import get_odds
from .stats import get_stats
from utils.logger import logger
from utils.page import block_junk, get_header_items, get_team_names
from utils.page import get_match_time, get_score
from utils.strings import extract_league_gameweek

async def process_game(page, is_future, is_league=True):
    caller = "GAME: process_game():-"
    home_link = await page.locator(".duelParticipant__home .participant__participantName a").first.get_attribute('href')
    away_link = await page.locator(".duelParticipant__away .participant__participantName a").first.get_attribute('href')
    country, league, round_ = await get_header_items(page, caller)
    home, away = await get_team_names(page, caller)
    match_time = await get_match_time(page, caller)
    match_odds = await get_odds(page, caller)
    h2h_stats = await get_h2h(page, home, caller, num=1)

    iter = extract_league_gameweek(round_)
    if is_league and iter:
        home_team_prev_matches = await get_previous_games(page, home_link, iter, is_league)
        away_team_prev_matches = await get_previous_games(page, away_link, iter, is_league)
    else:
        home_team_prev_matches = await get_previous_games(page, home_link, 7, is_league)
        away_team_prev_matches = await get_previous_games(page, away_link, 7, is_league)

    future_game = {}
    if is_future:
        round_ = iter if is_league else round_
        future_game['country'], future_game['league'], future_game['round'] = country, league, round_
        future_game['home_team'], future_game['away_team'] = home, away
        future_game['match_time'] = match_time
        for odd, v in match_odds.items():
            future_game[odd] = v            
        for h2h, v in h2h_stats.items():
            future_game[h2h] = v

    return (home_team_prev_matches + away_team_prev_matches), future_game
    

async def get_previous_games(page, link, iter, is_league):
    games = []
    try:
        await page.route("**/*", block_junk)
        await page.goto(f"https://www.flashscore.com{link}results/", wait_until="domcontentloaded", timeout=10000)
        events = await page.locator(".event__match").all()
        event_links = await get_links(events, "GAME: get_previous_games():- ")
        for i, href in enumerate(event_links[:iter]):
            match_details = await scrape_game(page, href, is_league)
            if not match_details:
                continue
            games.append(match_details)
            
    except Exception as e:
        logger.debug(f"GAME: Error fetching previous games {link}: {e}")    
    return games


async def scrape_game(page, href, is_league=True):
    caller = 'GAME: scrape_game():-'
    try:
        await page.goto(href, wait_until="domcontentloaded", timeout=10000)
        await page.wait_for_selector(".detail__breadcrumbs li", timeout=3000)
        country, league, round_ = await get_header_items(page, caller)
        gameweek = extract_league_gameweek(round_)

        # Only save league games
        if gameweek and is_league:
            match_dict = await get_prev_stat(page, caller, href, country, league, gameweek)
        else:
            match_dict = await get_prev_stat(page, caller, href, country, league, round_)
        
        return match_dict
    except Exception as e:
        logger.debug(f"{caller} {href}: {e}")
    finally:
        await page.go_back()
    return None


async def get_prev_stat(page, caller, href, country, league, round_):
    try:
        match_dict = {}
        home, away = await get_team_names(page, caller)            
        home_score, away_score = await get_score(page, caller)
        match_time = await get_match_time(page, caller)
        stats = await get_stats(page, caller)
        match_odds = await get_odds(page, caller)
        h2h_stats = await get_h2h(page, home, caller, num=0)
            
        if None in [home, away, home_score, away_score, match_time, stats, match_odds, h2h_stats]:
            logger.debug(f"{caller}{href} returns None's")
            return None
            
        match_dict['country'], match_dict['league'], match_dict['round'] = country, league, round_
        match_dict['home_team'], match_dict['away_team'] = home, away
        match_dict['match_time'] = match_time
        match_dict['home_score'], match_dict['away_score'] = home_score, away_score

        for stat, v in stats.items():
            match_dict[stat] = v

        for odd, v in match_odds.items():
            match_dict[odd] = v
            
        for h2h, v in h2h_stats.items():
            match_dict[h2h] = v
            
        return match_dict
    except Exception as e:
        logger.debug(f"{caller}{href}: {e}")