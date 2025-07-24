from utils.logger import logger
from utils.page import get_over_odds, get_1x2_odds, get_btts_odds, get_double_chance_odds


TAB_HANDLERS = {
    "Over/Under": get_over_odds,
    "1X2": get_1x2_odds,
    "Both teams to score": get_btts_odds,
    "Double chance": get_double_chance_odds,
}

async def get_odds(page, caller):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "Odds":
                return await click_odds_button(page, btn, caller)
                              
    except Exception as e:
        logger.debug(f"Error extracting stats: {e}")
    return None

async def click_odds_button(page, btn, caller):
    match_odds = {}
    try:
        await btn.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        await btn.click(timeout=5000)
        await page.wait_for_selector(
            ".container__livetable .container__detailInner .oddsTab__tableWrapper", timeout=5000
        )

        for tab_name, scrape_func in TAB_HANDLERS.items():
            try:
                buttons = await page.query_selector_all("button, [role='tab']")
                target_btn = None

                for b in buttons:
                    text = (await b.text_content() or "").strip()
                    if text == tab_name:
                        target_btn = b
                        break

                if not target_btn:
                    logger.warning(f"{caller} click_odds_button - Odds tab '{tab_name}' not found.")
                    continue

                await target_btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await target_btn.click(timeout=5000)
                await page.wait_for_selector(
                    ".container__livetable .container__detailInner .oddsTab__tableWrapper", timeout=5000
                )
                await page.wait_for_timeout(300)

                odds = await scrape_func(page, caller)
                for odd in odds:
                    if odd:
                        for k, v in odd.items():
                            key = f"{tab_name.lower().replace(' ', '_')}_{k}"
                            match_odds[key] = float(v)

            except Exception as e:
                logger.debug(f"{caller} click_odds_button - Failed on tab '{tab_name}': {e}")
                return None
        return match_odds
    except Exception as e:
        logger.debug(f"{caller} click_odds_button failed: {e}")

    return None

        

