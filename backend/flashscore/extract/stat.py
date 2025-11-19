import re
import asyncio
from flashscore.utils.logger import logger

def get_stats(page):
    try:
        buttons = page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (btn.text_content() or "").strip()
            if text == "Stats":
                btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                btn.click(timeout=5000)
                page.wait_for_selector(".container__livetable .container__detailInner .section", timeout=7000)
                return get_match_stats(page)
    except Exception as e:
        logger.debug(f"Error extracting stats: {e}")

def get_match_stats(page):
    stats = {}
    rows = page.locator(".wcl-row_2oCpS").all()

    for row in rows:
        try:
            category = (row.locator(".wcl-category_6sT1J").first.text_content() or "").strip()
            home_val = (row.locator(".wcl-homeValue_3Q-7P").first.text_content() or "").strip()
            away_val = (row.locator(".wcl-awayValue_Y-QR1").first.text_content() or "").strip()

            key_base = category.lower().replace(" ", "_") if category else "unknown"
            stats[f"home_{key_base}"] = get_digit_string(home_val)
            stats[f"away_{key_base}"] = get_digit_string(away_val)
        except Exception as e:
            continue

    return stats


def get_digit_string(text: str) -> str:
    text = re.sub(r"[%()/]", " ", text)
    text = text.split()[0] if text else ""
    return text.strip()
