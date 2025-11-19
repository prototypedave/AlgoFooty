# sync_scrape.py
import time
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from sqlalchemy import create_engine

from utils.logger import logger

# ----------------------------------------------------------------------
# Helper – block ads / images / fonts
def block_junk(route, request):
    if request.resource_type in {"image", "media", "font", "stylesheet"}:
        route.abort()
    elif "ads" in request.url or "analytics" in request.url:
        route.abort()
    else:
        route.continue_()

# ----------------------------------------------------------------------
def scrape_previous_game(context, href: str, prev: bool) -> Optional[Dict]:
    """Open a fresh page, scrape one past match, then close it."""
    page = context.new_page()
    try:
        page.route("**/*", block_junk)
        page.goto(href, wait_until="domcontentloaded", timeout=15000)

        # ----- very small subset – replace with your real getters -----
        home = page.locator(".duelParticipant__home .participant__participantName a").first.inner_text()
        away = page.locator(".duelParticipant__away .participant__participantName a").first.inner_text()
        # ----------------------------------------------------------------

        logger.info(f"  [PREV] {home} vs {away}")
        return {"home": home, "away": away, "url": href}
    except PWTimeout:
        logger.warning(f"  [PREV] timeout {href}")
        return None
    except Exception as e:
        logger.debug(f"  [PREV] error {href}: {e}")
        return None
    finally:
        page.close()

# ----------------------------------------------------------------------
def process_main_match(page, context) -> tuple[List[Dict], Optional[Dict]]:
    """Scrape the main duel page (the one you land on from the list)."""
    try:
        # ----- main-match data ------------------------------------------------
        home = page.locator(".duelParticipant__home .participant__participantName a").first.inner_text()
        away = page.locator(".duelParticipant__away .participant__participantName a").first.inner_text()
        logger.info(f"Processing {home} v {away}")

        # ----- previous games (1 per team) ------------------------------------
        prev_games = []

        # team links
        home_link = page.locator(".duelParticipant__home .participant__participantName a").first.get_attribute("href")
        away_link = page.locator(".duelParticipant__away .participant__participantName a").first.get_attribute("href")

        # open the *team results* page once, grab the first N match links
        team_page = context.new_page()
        team_page.route("**/*", block_junk)

        # home team
        team_page.goto(f"https://www.flashscore.com{home_link}results/", timeout=15000)
        links = [a.get_attribute("href") for a in team_page.locator(".event__match a").all()[:1]]
        team_page.close()

        for href in links:
            full = f"https://www.flashscore.com{href}"
            d = scrape_previous_game(context, full, prev=True)
            if d:
                prev_games.append(d)

        # away team – repeat the same logic (omitted for brevity)

        # ----- future-game dict ------------------------------------------------
        future = {"home": home, "away": away, "match_time": datetime.now()}
        return prev_games, future

    except Exception as e:
        logger.error(f"Main match error: {e}")
        return [], None

# ----------------------------------------------------------------------
def main():
    engine = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
    batch: List[Dict] = []
    pred_batch: List[Dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
                                    args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            timezone_id="America/New_York"
        )

        # ---- open the calendar page once ------------------------------------
        calendar = context.new_page()
        calendar.route("**/*", block_junk)
        calendar.goto("https://www.flashscore.com/", timeout=15000)

        # (optional) click a few “next day” buttons – sync version is trivial
        # ---------------------------------------------------------------------

        # ---- collect every match link on the current day --------------------
        calendar.wait_for_selector(".event__match", timeout=8_000)
        match_elements = calendar.locator(".event__match a").all()
        raw_hrefs = [e.get_attribute("href") for e in match_elements]

        links = []
        base = "https://www.flashscore.com"
        for href in raw_hrefs:
            if href and not href.startswith("javascript:"):
                full_url = urljoin(base, href)
                links.append(full_url)

        logger.info(f"Found {len(links)} valid matches")

        # ---- process them one-by-one (no asyncio, no semaphore) ------------
        for idx, href in enumerate(links, 1):
            full_url = href  # already full URL
            page = context.new_page()


            try:
                page.goto(full_url, wait_until="domcontentloaded", timeout=15000)
                prev, fut = process_main_match(page, context)
                if prev:
                    batch.extend(prev)
                if fut:
                    pred_batch.append(fut)

                logger.info(f"[{idx}/{len(links)}] DONE – {href.split('/')[-2]}")
            except PWTimeout:
                logger.warning(f"Timeout on {full_url}")
            except Exception as e:
                logger.error(f"Unexpected error {full_url}: {e}")
            finally:
                page.close()

            # ---- flush to DB every 10 records --------------------------------
            if len(batch) >= 10:
                df = pd.DataFrame(batch).drop_duplicates(
                    subset=["home", "away", "match_time"]
                )
                df.to_sql("new_league", con=engine, if_exists="append", index=False)
                batch.clear()
                logger.info("DB flush (new_league)")

        # final flush
        if batch:
            pd.DataFrame(batch).to_sql("new_league", con=engine, if_exists="append", index=False)
        if pred_batch:
            pd.DataFrame(pred_batch).to_sql("new_pred", con=engine, if_exists="append", index=False)

        context.close()
        browser.close()

    logger.info("Scraping finished")

if __name__ == "__main__":
    start = time.time()
    main()
    logger.info(f"Total time: {(time.time() - start):.1f}s")