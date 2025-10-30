from datetime import datetime, timedelta
from extract.event import get_events
from extract.game import process_game
from extract.navigate import navigate_to_page
from extract.scrape_utils import block_junk
from playwright.async_api import async_playwright
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from typing import List, Dict
from utils.logger import logger
import asyncio
import pandas as pd

class FlashscoreApp:
    def __init__(self, concurrency: int=3) -> None:
        self.browser = None
        self.context = None
        self.playwright = None
        self.semaphore = asyncio.Semaphore(concurrency)
        self.batch: List[Dict] = []
        self.pred_batch: List[Dict] = []
        self.batch_size = 10
        self.is_future = False
        self.engine = None  

    async def start(self) -> None:
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                timezone_id="America/New_York"
            )
            self.engine = create_engine("postgresql+psycopg2://postgres:your_password@localhost:5432/final")
            logger.info("FLASHSCORE: Success:- Flashscore App started")
        except Exception as e:
            logger.info(f"FLASHSCORE: Error:- {e}")
            raise

    async def save_batch(self) -> None:
        try:
            games = pd.DataFrame(self.batch)
            games = games.drop_duplicates(subset=["home_team", "away_team", "match_time"])
            
            if not games.empty:
                games.to_sql("new_league", con=self.engine, if_exists="append", index=False)
                '''metadata = MetaData()
                table = Table("new_league", metadata, autoload_with=self.engine)

                with self.engine.begin() as conn:
                    for _, row in games.iterrows():
                        stmt = insert(table).values(**row.to_dict())
                        
                        stmt = stmt.on_conflict_do_update(
                            index_elements=["home_team", "away_team", "match_time"],
                            set_={
                                col: stmt.excluded[col]
                                for col in row.index
                                if col not in ["home_team", "away_team", "match_time"]
                            },
                        )

                        conn.execute(stmt)'''

            logger.info("DB: updated games table")

            if self.pred_batch:
                pred = pd.DataFrame(self.pred_batch)
                pred.to_sql("new_pred", con=self.engine, if_exists="append", index=False)
            
            self.batch.clear()
            self.pred_batch.clear()

        except Exception as e:
            logger.error(f"DB: Error:- {e}")
        
    async def stop(self):
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            await self.save_batch()
            self.engine = None
            logger.info("FLASHSCORE: Browser stopped successfully.")
        except Exception as e:
            print(f"{e}")

    async def run_app(self, days=0):
        url = "https://www.flashscore.com/"
        if not self.context:
            raise RuntimeError("App not started yet")   
        page = await self.context.new_page()
        if not page:
            raise RuntimeError("Failed to create new page")
        
        try:
            try:
                await page.route("**/*", block_junk)
            except Exception as e:
                logger.error(f"FLASHSCORE: Failed to configure routing: {e}")
            
            self.is_future = True if days >= 0 else False
            await page.goto(url)
            days = abs(days)
            if days > 0:
                await navigate_to_page(page, self.is_future, days)
            game_links = await get_events(page)
            await self.load_events(game_links)

        except Exception as e:
            logger.error(f"FLASHSCORE: Error:- {e}")
        
    async def load_events(self, events):
        batch_size = 5
        for i in range(0, len(events), batch_size):
            batch = events[i:i + batch_size]
            tasks = [self.load_game(link) for link in batch]
            await asyncio.gather(*tasks, return_exceptions=True)

    async def load_game(self, link):
        async with self.semaphore:
            page = await self.context.new_page()
            if not page:
                logger.error(f"GAME: Warn:- failed to create page for {link}")
                return None
            try:
                await page.route("**/*", block_junk)
                await page.goto(link, timeout=10000)
                prev_games, future_game = await process_game(page)
                if prev_games:
                    self.batch += prev_games
                    if len(self.batch) >= self.batch_size:
                        await self.save_batch()
                if future_game:
                    self.pred_batch.append(future_game)
                
            except Exception as e:
                logger.error(f"GAME: Error processing {link}: {e}")
                return None
            finally:
                await page.close()

    async def get_data_from_db(self):
        df = pd.read_sql("SELECT * FROM league_games", con=self.engine)
        today = (datetime.now() - timedelta(days=2)).date()
        query = f"""
            SELECT *
            FROM new_league
            WHERE DATE(match_time) = '{today}'
            """
        pred = pd.read_sql(query, con=self.engine)
        return df, pred
    

if __name__ == "__main__":
    async def main():
        app = FlashscoreApp(concurrency=2)
        await app.start()
        await app.run_app(days=0)
        
        await app.stop()

    asyncio.run(main())