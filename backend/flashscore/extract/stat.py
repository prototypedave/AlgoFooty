import re
import asyncio
from utils.logger import logger

async def get_stats(page):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "Stats":
                await btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await btn.click(timeout=5000)
                await page.wait_for_selector(".container__livetable .container__detailInner .section", timeout=7000)
                return await get_match_stats(page)
    except Exception as e:
        logger.debug(f"Error extracting stats: {e}")

async def get_match_stats(page):
    stats = {}
    rows = await page.locator(".wcl-row_2oCpS").all()
    tasks = []
    for row in rows:
        async def extract_row(row):
            try:
                category = await row.locator(".wcl-category_6sT1J").first.text_content()
                home_val = await row.locator(".wcl-homeValue_3Q-7P").first.text_content()
                away_val = await row.locator(".wcl-awayValue_Y-QR1").first.text_content()
                return {
                    f"home_{category.lower().replace(' ', '_')}": get_digit_string(home_val),
                    f"away_{category.lower().replace(' ', '_')}": get_digit_string(away_val)
                }
            except:
                return {}
        tasks.append(extract_row(row))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, dict):
            stats.update(result)
    return stats

def get_digit_string(text: str) -> str:
    text = re.sub(r"[%()/]", " ", text)
    text = text.split()[0] if text else ""
    return text.strip()