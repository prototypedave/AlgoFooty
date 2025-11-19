from flashscore.extract.event import get_links
from flashscore.extract.h2h import get_h2h
from flashscore.extract.odd import get_odds
from flashscore.extract.scrape_utils import *
from flashscore.extract.standings import get_standings
from flashscore.extract.stat import get_stats
from flashscore.utils.logger import logger


def process_game(page):
    try:
        home_link = page.locator(".duelParticipant__home .participant__participantName a").first.get_attribute('href')
        away_link = page.locator(".duelParticipant__away .participant__participantName a").first.get_attribute('href')
        home_img = page.locator(".duelParticipant__home .participant__image").first.get_attribute('src')
        away_img = page.locator(".duelParticipant__away .participant__image").first.get_attribute('src')

        country, league, round_ = get_header_items(page)
        home, away = get_team_names(page)
        match_time = get_match_time(page)
        match_odds = get_odds(page)
        h2h_stats = get_h2h(page, home, away, num=4)
        standings = get_standings(page, home, away)
        
        home_team_prev_matches = get_previous_games(page, home_link, 1, prev=True)
        away_team_prev_matches = get_previous_games(page, away_link, 1, prev=True)

        if non_league_games(league, round_):
            return None, None
        
        if not match_odds or not h2h_stats:
            return None, None
        
        future_game = {}
        future_game['country'], future_game['league'], future_game['round'] = country, league, round_
        future_game['home_team'], future_game['away_team'] = home, away
        future_game['match_time'] = match_time
        future_game['home_img'], future_game['away_img'] = home_img, away_img

        for odd, v in match_odds.items():
            future_game[odd] = v            
        for h2h, v in h2h_stats.items():
            future_game[h2h] = v
        for stan, v in standings.items():
            future_game[stan] = v

        logger.info(f"GAME: Successfully processed {home} v {away}")
        return (home_team_prev_matches + away_team_prev_matches), future_game

    except Exception as e:
        logger.debug(f'{e}')
        return None, None


def get_previous_games(page, link, iter, prev):
    games = []
    try:
        page.route("**/*", block_junk)
        page.goto(f"https://www.flashscore.com{link}results/", timeout=10000)
        events = page.locator(".event__match").all()
        event_links = get_links(events)
        for i, href in enumerate(event_links[:iter]):
            match_details = scrape_game(page, href, prev)
            if not match_details:
                continue
            games.append(match_details.copy())
            
    except Exception as e:
        logger.debug(f"GAME: Error fetching previous games {link}: {e}")  
    return games


def scrape_game(page, href, prev):
    try:
        page.goto(href, wait_until="domcontentloaded", timeout=10000)
        page.wait_for_selector(".detail__breadcrumbs li", timeout=3000)
        country, league, round_ = get_header_items(page)
        if non_league_games(league, round_):
            return None
        match_dict = get_prev_stat(page, href, country, league, round_, prev)
        return match_dict
    except Exception as e:
        logger.debug(f"{href}: {e}")
    finally:
        try:
            page.go_back()
        except:
            pass
    return None


def get_prev_stat(page, href, country, league, round_, prev):
    try:
        match_dict = {}
        home, away = get_team_names(page)            
        home_score, away_score = get_score(page)
        match_time = get_match_time(page)
        stats = get_stats(page)
        match_odds = get_odds(page)
        h2h_stats = get_h2h(page, home, away, num=4, prev=prev)
        standings = get_standings(page, home, away)

        if None in [home, away, home_score, away_score, match_time, match_odds, h2h_stats]:
            logger.debug(f"{href} returns None's")
            return None
            
        match_dict['country'], match_dict['league'], match_dict['round'] = country, league, round_
        match_dict['home_team'], match_dict['away_team'] = home, away
        match_dict['match_time'] = match_time
        match_dict['home_score'], match_dict['away_score'] = home_score, away_score

        for odd, v in match_odds.items():
            match_dict[odd] = v
        for h2h, v in h2h_stats.items():
            match_dict[h2h] = v
        for stat, v in stats.items():
            match_dict[stat] = v
        for stan, v in standings.items():
            match_dict[stan] = v
            
        return match_dict
    except Exception as e:
        logger.debug(f"{href}: {e}")
        return None


def non_league_games(league, round):
    if not league or "cup" in league.lower() or not round:
        return True
    
    non_league = ["none", "trophy", "finals", "play-off", "playoff", "semifinals", "semi-finals", "semi", "quarter"]
    for non in non_league:
        if non in round.lower():
            return True
        
    return False
