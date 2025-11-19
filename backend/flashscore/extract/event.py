from flashscore.utils.logger import logger

def get_events(page):
    page.wait_for_selector(".event__match", timeout=5000)
    events = page.locator(".event__match").all()
    logger.info(f"Found {len(events)} matches")
    return get_links(events)

def get_links(events):
    links = []
    for event in events:
        try:
            href = event.locator("a").first.get_attribute("href")
            if href:
                links.append(href)
        except Exception as e:
            logger.error(f"Error getting link: {e}")
    return links
