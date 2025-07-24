from utils.logger import logger
from utils.strings import split_value

async def get_h2h(page, home, caller, num):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "H2H":
                await btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await btn.click(timeout=5000)
                await page.wait_for_selector(".container__livetable .container__detailInner .h2h__section", timeout=5000)
                return await get_h2h_stats(page, home, caller, num) 
                
    except Exception as e:
        logger.debug(f"Error extracting stats: {e}")
    return None

async def get_h2h_stats(page, checker, caller, num):
    h2h_stats = {
        'h2h_over_15': None,
        'h2h_home_over_15': None,
        'h2h_away_over_15': None,
        'h2h_over_25': None,
        'h2h_home_over_25': None,
        'h2h_away_over_25': None,
        'h2h_under_35': None,
        'h2h_home_under_35': None,
        'h2h_away_under_35': None,
        'h2h_team_home_win': None,
        'h2h_team_away_win': None,
        'h2h_home_win': None,
        'h2h_away_win': None,
        'h2h_btts': None,
        'h2h_home_btts': None,
        'h2h_away_btts': None
    }

    try:
        h2h_sections = await page.locator(".h2h__section").all()
        if len(h2h_sections) != 3:
            return None

        h2h_games = await h2h_sections[2].locator(".rows .h2h__row").all()
        if len(h2h_games) <= num:
            return None

        stats = {
            "over_15": 0, "over_15_home": 0, "over_15_away": 0,
            "over_25": 0, "over_25_home": 0, "over_25_away": 0,
            "under_35": 0, "under_35_home": 0, "under_35_away": 0,
            "home_team_wins": 0, "away_team_wins": 0,
            "team_home_wins": 0, "team_away_wins": 0,
            "btts": 0, "btts_home": 0, "btts_away": 0
        }

        for game in h2h_games:
            home = (await game.locator(".h2h__homeParticipant").text_content() or "").strip()
            away = (await game.locator(".h2h__awayParticipant").text_content() or "").strip()
            result = (await game.locator(".h2h__result").text_content() or "").strip()
            home_score, away_score = split_value(result)
            total = home_score + away_score

            if total > 1.5:
                stats["over_15"] += 1
                if home == checker:
                    stats["over_15_home"] += 1
                elif away == checker:
                    stats["over_15_away"] += 1

            if total > 2.5:
                stats["over_25"] += 1
                if home == checker:
                    stats["over_25_home"] += 1
                elif away == checker:
                    stats["over_25_away"] += 1

            if total < 4:
                stats["under_35"] += 1
                if home == checker:
                    stats["under_35_home"] += 1
                elif away == checker:
                    stats["under_35_away"] += 1

            if (home == checker and home_score > away_score) or (away == checker and away_score > home_score):
                stats["home_team_wins"] += 1
            if (home != checker and away_score > home_score) or (away != checker and home_score > away_score):
                stats["away_team_wins"] += 1
            if home == checker and home_score > away_score:
                stats["team_home_wins"] += 1
            if away != checker and away_score > home_score:
                stats["team_away_wins"] += 1

            if home_score > 0 and away_score > 0:
                stats["btts"] += 1
                if home == checker:
                    stats["btts_home"] += 1
                elif home != checker:
                    stats["btts_away"] += 1

        num_games = len(h2h_games)

        h2h_stats.update({
            "h2h_over_15": stats["over_15"] / num_games,
            "h2h_home_over_15": stats["over_15_home"] / num_games,
            "h2h_away_over_15": stats["over_15_away"] / num_games,
            "h2h_over_25": stats["over_25"] / num_games,
            "h2h_home_over_25": stats["over_25_home"] / num_games,
            "h2h_away_over_25": stats["over_25_away"] / num_games,
            "h2h_under_35": stats["under_35"] / num_games,
            "h2h_home_under_35": stats["under_35_home"] / num_games,
            "h2h_away_under_35": stats["under_35_away"] / num_games,
            "h2h_team_home_win": stats["home_team_wins"] / num_games,
            "h2h_team_away_win": stats["away_team_wins"] / num_games,
            "h2h_home_win": stats["team_home_wins"] / num_games,
            "h2h_away_win": stats["team_away_wins"] / num_games,
            "h2h_btts": stats["btts"] / num_games,
            "h2h_home_btts": stats["btts_home"] / num_games,
            "h2h_away_btts": stats["btts_away"] / num_games,
        })

        logger.debug(f"{caller} get_h2h_stats : {h2h_stats}")
        return h2h_stats

    except Exception as e:
        logger.debug(f"{caller} get_h2h_stats : {e}")
        return None


    



