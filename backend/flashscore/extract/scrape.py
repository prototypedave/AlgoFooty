from datetime import datetime, timedelta
from flashscore.extract.event import get_events
from flashscore.extract.game import process_game
from flashscore.extract.navigate import navigate_to_page
from flashscore.extract.scrape_utils import block_junk
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from sqlalchemy import create_engine
from flashscore.utils.logger import logger
import pandas as pd
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

class FlashscoreApp:
    def __init__(self, concurrency: int = 3) -> None:
        self.concurrency = concurrency
        self.batch: List[Dict] = []
        self.pred_batch: List[Dict] = []
        self.batch_size = 10
        self.engine = None

    def start(self) -> None:
        try:
            self.engine = create_engine(os.getenv("DB_CONN"))
            logger.info("FLASHSCORE: Success:- Flashscore App started (DB connected)")
        except Exception as e:
            logger.error(f"DB: Connection failed: {e}")
            raise

    def save_batch(self) -> None:
        try:
            if self.batch:
                games = pd.DataFrame(self.batch).drop_duplicates(subset=["home_team", "away_team", "match_time"])
                if not games.empty:
                    games.to_sql(os.getenv("LEAGUE_DB_TABLE"), con=self.engine, if_exists="append", index=False)
                    logger.info(f"DB: Flushed {len(games)} games to new_league")
                self.batch.clear()

            if self.pred_batch:
                pred = pd.DataFrame(self.pred_batch)
                pred.to_sql(os.getenv("PREDICTION_TABLE"), con=self.engine, if_exists="append", index=False)
                logger.info(f"DB: Flushed {len(pred)} predictions to new_pred")
                self.pred_batch.clear()

        except Exception as e:
            logger.error(f"DB: Save error: {e}")

    def stop(self):
        self.save_batch()
        self.engine = None
        logger.info("FLASHSCORE: App stopped and final batch saved.")

    def run_app(self, days: int = 0):
        url = os.getenv("SCRAPE_URL")
        playwright = sync_playwright().start()
        browser = None
        context = None

        try:
            browser = playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            )

            context = browser.new_context(
                user_agent=user_agent,
                timezone_id="America/New_York"
            )

            page = context.new_page()
            page.route("**/*", block_junk)
            page.goto(url, timeout=7000)

            is_future = days >= 0
            days = abs(days)
            if days > 0:
                navigate_to_page(page, is_future, days)

            game_links = get_events(page)
            page.close()

            logger.info(f"Found {len(game_links)} match links. Starting parallel scraping...")
            self._scrape_parallel(game_links, user_agent)

        except Exception as e:
            logger.error(f"FLASHSCORE: Fatal error: {e}")
        finally:
            if context:
                context.close()
            if browser:
                browser.close()
            playwright.stop()

    def _scrape_parallel(self, links: List[str], user_agent: str):
        def worker(link: str) -> Tuple[List[Dict], Dict | None]:
            p = sync_playwright().start()
            try:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
                )
                context = browser.new_context(
                    user_agent=user_agent,
                    timezone_id="America/New_York"
                )
                page = context.new_page()
                page.route("**/*", block_junk)

                try:
                    page.goto(link, wait_until="domcontentloaded", timeout=10000)
                    prev_games, future_game = process_game(page)
                    return prev_games or [], future_game
                except PWTimeout:
                    logger.warning(f"Timeout: {link}")
                    return [], None
                except Exception as e:
                    logger.error(f"Error processing {link}: {e}")
                    return [], None
                finally:
                    page.close()
                    context.close()
                    browser.close()
            finally:
                p.stop()
            return [], None

        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = {executor.submit(worker, link): link for link in links}

            for idx, future in enumerate(as_completed(futures), 1):
                link = futures[future]
                try:
                    prev_games, future_game = future.result()
                    if prev_games:
                        self.batch.extend(prev_games)
                    if future_game:
                        self.pred_batch.append(future_game)

                    if len(self.batch) >= self.batch_size:
                        self.save_batch()

                    logger.info(f"[{idx}/{len(links)}] DONE – {urllib.parse.urlparse(link).path.split('/')[-2]}")
                except Exception as e:
                    logger.error(f"Future failed for {link}: {e}")

        self.save_batch()


if __name__ == "__main__":
    app = FlashscoreApp(concurrency=2)
    app.start()
    app.run_app(days=-2)
    app.stop()
