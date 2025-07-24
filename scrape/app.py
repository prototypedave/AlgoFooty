# Scrape Class App
from .events import get_events
from playwright.async_api import async_playwright

from utils.logger import logger
from utils.page import block_junk

import asyncio

class Scraper:
    def __init__(self, concurrency: int = 3):
        self.browser = None
        self.context = None
        self.playwright = None
        self.semaphore = asyncio.Semaphore(concurrency)

    async def start(self):
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            logger.info("APP: FlashScore App Started Successfully")            
        except Exception as e:
            logger.error(f"APP: Flashscore failed to start: {e}")
            raise

    async def stop(self):
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"APP: Encountered error while closing Flashscore App: {e}")

    async def load_flashscore(self, url: str = "https://www.flashscore.com/"):
        if not self.context:
            raise RuntimeError("Browser context not initialized")    
        page = await self.context.new_page()
        if not page:
            raise RuntimeError("Failed to create new page")

        try:
            try:
                await page.route("**/*", block_junk)
            except Exception as e:
                logger.warning(f"FLASHSCORE: Failed to configure routing: {e}")
            await page.goto(url)
            event_links = await get_events(page, "FLASHSCORE:")
            print(event_links)
                   
        except Exception as e:
            logger.error(f"FLASHSCORE: Error loading main page {url}: {e}")
            raise
        finally:
            await page.close()