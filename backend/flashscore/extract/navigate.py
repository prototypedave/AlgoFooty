from utils.logger import logger

async def navigate_to_page(page, future, days=0):
    if days > 7:
        logger.error(f"{days} days is larger than the allowed navigation days, defaulting to 7")
        days = 7

    aria_label = 'Next day' if future else 'Previous day'
    for day in range(days):
        try:
            btn = await page.wait_for_selector(f'button[aria-label="{aria_label}"]', timeout=5000)
            if not btn:
                logger.error(f'FLASHSCORE: Navigation button "{aria_label}" not found!')
                continue

            current_date = await get_flashscore_date(page)

            await btn.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            await btn.click(timeout=5000)

            await page.wait_for_function(
                """(prevDate) => {
                    const el = document.querySelector(".wcl-button_mrGAO");
                    return el && el.textContent.trim() !== prevDate;
                }""",
                arg=current_date,
                timeout=10000
            )

            new_date = await get_flashscore_date(page)
            logger.info(f"FLASHSCORE : Navigated successfully: {new_date}")

        except Exception as e:
            logger.error(f"FLASHSCORE: Failed to navigate to day {day + 1}: {e}")
            raise RuntimeError(f"FLASHSCORE: Navigation failed on day {day + 1}")
    
    return page


async def get_flashscore_date(page):
    try:
        el = await page.wait_for_selector(".wcl-button_mrGAO", timeout=5000)
        return (await el.text_content()).strip()
    except:
        return "Unknown"


def is_navigation(move, days):
    if move and days > 0:
        return True
    return False