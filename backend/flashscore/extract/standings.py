from utils.logger import logger

async def get_standings(page, home, away):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "Standings":
                await btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await btn.click(timeout=5000)
                await page.wait_for_selector(".tableWrapper", timeout=7000)
                return await extract_standings(page, home, away)
    except Exception as e:
        logger.debug(f"Error extracting standings: {e}")


async def extract_standings(page, home, away):
    standings = {}
    try:
        rows = await page.locator(".table__row--selected").all()
        for row in rows:
            try:
                team_name = (await row.locator(".table__cell--participant").first.text_content() or "").strip()
                team_rank = (await row.locator(".tableCellRank").first.text_content() or "").strip().rstrip('.')
                if team_name:    
                    prefix = "home" if team_name == home else "away"
                    metrics = await row.locator(".table__cell--value").all()
                    standings[prefix + "_rank"] = int(team_rank)
                    standings[prefix + "_games_played"] = int((await metrics[0].text_content() or "").strip())
                    standings[prefix + "_games_won"] = int((await metrics[1].text_content() or "").strip())
                    standings[prefix + "_games_drawn"] = int((await metrics[2].text_content() or "").strip())
                    standings[prefix + "_games_lost"] = int((await metrics[3].text_content() or "").strip())
                    standings[prefix + "_games_goals_scored"], standings[prefix + "_games_goals_conceded"] = split_score((await metrics[4].text_content() or "").strip())
                    standings[prefix + "_games_goal_diff"] = int((await metrics[5].text_content() or "").strip())
                    standings[prefix + "_games_points"] = int((await metrics[6].text_content() or "").strip())
                    
            except Exception as e:
                logger.debug(f"extract_standings: Error getting team name: {e}")
                continue
    except Exception as e:
        logger.debug(f"extract_standings: {e}")
    return standings

def split_score(score):
    if not score:
        return None, None
    parts = score.split(":")
    return int(parts[0].strip()), int(parts[1].strip()) if len(parts) == 2 else (None, None)