from flashscore.utils.logger import logger

def get_standings(page, home, away):
    try:
        buttons = page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (btn.text_content() or "").strip()
            if text == "Standings":
                btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                btn.click(timeout=5000)
                page.wait_for_selector(".tableWrapper", timeout=7000)
                return extract_standings(page, home, away)
    except Exception as e:
        logger.debug(f"Error extracting standings: {e}")


def extract_standings(page, home, away):
    standings = {}
    try:
        rows = page.locator(".table__row--selected").all()
        for row in rows:
            try:
                team_name = (row.locator(".table__cell--participant").first.text_content() or "").strip()
                team_rank = (row.locator(".tableCellRank").first.text_content() or "").strip().rstrip('.')
                if team_name:    
                    prefix = "home" if team_name == home else "away"
                    metrics = row.locator(".table__cell--value").all()
                    standings[prefix + "_rank"] = int(team_rank)
                    standings[prefix + "_games_played"] = int((metrics[0].text_content() or "").strip())
                    standings[prefix + "_games_won"] = int((metrics[1].text_content() or "").strip())
                    standings[prefix + "_games_drawn"] = int((metrics[2].text_content() or "").strip())
                    standings[prefix + "_games_lost"] = int((metrics[3].text_content() or "").strip())
                    standings[prefix + "_games_goals_scored"], standings[prefix + "_games_goals_conceded"] = split_score((metrics[4].text_content() or "").strip())
                    standings[prefix + "_games_goal_diff"] = int((metrics[5].text_content() or "").strip())
                    standings[prefix + "_games_points"] = int((metrics[6].text_content() or "").strip())
                    
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
