# App
from scrape.app import Scraper

import asyncio

async def main():
    scrape = Scraper()
    await scrape.start()
    await scrape.load_flashscore(days=8, move='prev')
    await scrape.stop()

if __name__ == '__main__':
    asyncio.run(main())