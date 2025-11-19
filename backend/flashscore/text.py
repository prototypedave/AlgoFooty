import asyncio

from playwright.async_api import async_playwright
from .utils.scrape_utils import block_junk
from .utils.navigate import navigate_to_page
from .utils.event import get_events

class FlashScoreApp:
    def __init__(self, conc: int=3) -> None:
        self.browser = None
        self.context = None
        self.playwright = None
        self.semaphore = asyncio.Semaphore(conc)

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
        except Exception as e:
            raise

    async def stop(self):
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.engine = None
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
                print(e)
            
            self.is_future = True if days >= 0 else False
            await page.goto(url)
            days = abs(days)
            if days > 0:
                await navigate_to_page(page, self.is_future, days)
            game_links = await get_events(page)
            await self.load_events(game_links[600:])

        except Exception as e:
            print(e)
        
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
                print(f"GAME: Warn:- failed to create page for {link}")
                return None
            try:
                await page.route("**/*", block_junk)
                await page.goto(link, timeout=10000)
                
            except Exception as e:
                print(f"GAME: Error processing {link}: {e}")
                return None
            finally:
                await page.close()


if __name__ == "__main__":
    async def main():
        app = FlashScoreApp(conc=1)
        await app.start()
        await app.run_app(days=1)
        
        await app.stop()

    asyncio.run(main())