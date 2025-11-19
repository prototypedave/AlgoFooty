from flashscore.extract.scrape_utils import split_value
from flashscore.utils.logger import logger
import asyncio
import numpy as np


def get_h2h(page, home, away, num, prev=False):
    try:
        buttons = page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (btn.text_content() or "").strip()
            if text == "H2H":
                btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                btn.click(timeout=5000)
                page.wait_for_selector(".container__livetable .container__detailInner .h2h__section", timeout=7000)
                return get_h2h_stats(page, home, away, num, prev) 
                
    except Exception as e:
        logger.debug(f"H2H: Error extracting stats: {e}")
    return None


def get_h2h_stats(page, home, away, num, prev):
    stats = {}
    try:
        h2h_sections = page.locator(".h2h__section").all()
        if len(h2h_sections) != 3:
            return None

        home_games = h2h_sections[0].locator(".rows .h2h__row").all()
        away_games = h2h_sections[1].locator(".rows .h2h__row").all()
        h2h_games = h2h_sections[2].locator(".rows .h2h__row").all()

        if any(len(games) <= num for games in [home_games, away_games, h2h_games]):
            return None

        if prev:
            home_games = home_games[1:]
            away_games = away_games[1:]
            h2h_games = h2h_games[1:]
        else:
            home_games = home_games[:4]
            away_games = away_games[:4]
            h2h_games = h2h_games[:4]

        stats = get_head(home_games, home, 'home', stats)
        stats = get_head(away_games, away, 'away', stats)
        stats = get_head(h2h_games, home, 'h2h', stats)

        return stats

    except Exception as e:
        logger.debug(f"H2H: get_h2h_stats : {e}")
        return None


def get_head(games, team, prefix, stats):
    def extract_game(i, game):
        try:
            home = (game.locator(".h2h__homeParticipant").text_content() or "").strip()
            away = (game.locator(".h2h__awayParticipant").text_content() or "").strip()
            result = (game.locator(".h2h__result").text_content() or "").strip()
        except Exception:
            return {}

        home_score, away_score = split_value(result)

        if home == team:
            return {
                f"{prefix}_h_score_{i}": home_score,
                f"{prefix}_o_score_{i}": away_score,
                f"{prefix}_side_{i}": 1
            }
        elif away == team:
            return {
                f"{prefix}_h_score_{i}": away_score,
                f"{prefix}_o_score_{i}": home_score,
                f"{prefix}_side_{i}": 0
            }
        return {}

    for i, game in enumerate(games):
        result = extract_game(i, game)
        stats.update(result)

    return stats
