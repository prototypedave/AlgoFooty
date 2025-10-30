from extract.scrape_utils import split_value
from utils.logger import logger
import asyncio
import numpy as np


async def get_h2h(page, home, away, num, prev=False):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "H2H":
                await btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await btn.click(timeout=5000)
                await page.wait_for_selector(".container__livetable .container__detailInner .h2h__section", timeout=7000)
                return await get_h2h_stats(page, home, away, num, prev) 
                
    except Exception as e:
        logger.debug(f"H2H: Error extracting stats: {e}")
    return None

async def get_h2h_stats(page, home, away, num, prev):
    stats = {}
    try:
        
        h2h_sections = await page.locator(".h2h__section").all()
        if len(h2h_sections) != 3:
            return None
        
        home_games = await h2h_sections[0].locator(".rows .h2h__row").all()
        if len(home_games) <= num:
            return None
        
        h2h_games = await h2h_sections[2].locator(".rows .h2h__row").all()
        if len(h2h_games) <= num:
            return None
        
        away_games = await h2h_sections[1].locator(".rows .h2h__row").all()
        if len(away_games) <= num:
            return None
        
        if prev:
            home_games = home_games[1:]
            away_games = away_games[1:]
            h2h_games = h2h_games[1:]
        else:
            home_games = home_games[:4]
            away_games = away_games[:4]
            h2h_games = h2h_games[:4]
        
        home_task = asyncio.create_task(get_head(home_games, home, 'home', stats))
        away_task = asyncio.create_task(get_head(away_games, away, 'away', stats))
        h2h_task = asyncio.create_task(get_head(h2h_games, home, 'h2h', stats))

        results = await asyncio.gather(home_task, away_task, h2h_task)
        for r in results:
            stats.update(r)
        return stats
    except Exception as e:
        logger.debug(f"H2H: get_h2h_stats : {e}")
        return None


async def get_head(games, team, prefix, stats):
    async def extract_game(i, game):
        home, away, result = await asyncio.gather(
            game.locator(".h2h__homeParticipant").text_content(),
            game.locator(".h2h__awayParticipant").text_content(),
            game.locator(".h2h__result").text_content()
        )

        home = (home or "").strip()
        away = (away or "").strip()
        result = (result or "").strip()
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

    results = await asyncio.gather(*(extract_game(i, g) for i, g in enumerate(games)))
    for r in results:
        stats.update(r)
    return stats