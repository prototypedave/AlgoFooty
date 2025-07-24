from utils.logger import logger
import asyncio

async def get_events(page, caller):
    await page.wait_for_selector(".event__match", timeout=5000)
    events = await page.locator(".event__match").all()
    logger.info(f"{caller} Found {len(events)} matches")
    return await get_links(events, caller)

async def get_links(events, caller):
    async def get_link(event):
        try:
            return await event.locator("a").first.get_attribute("href")
        except Exception as e:
            logger.debug(f"{caller} Error getting link: {e}")
            return None
    links = await asyncio.gather(*[get_link(e) for e in events])
    return [link for link in links if link]