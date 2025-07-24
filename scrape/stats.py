from utils.links import assemble_url
from utils.logger import logger
from utils.strings import get_digit_string

async def get_stats(page, caller):
    caller += "get_stats() - "
    try:
        stats_url = assemble_url(caller, page.url, "/match-statistics/0")
        await page.goto(stats_url, wait_until="domcontentloaded", timeout=5000)
        await page.wait_for_selector(".container__livetable .container__detailInner .section", timeout=10000)
        return await get_match_stats(page, caller)
    except Exception as e:
        logger.debug(f"{caller}{e}")
    finally:
        try:
            await page.go_back(wait_until="domcontentloaded", timeout=3000)
        except Exception as e:
            logger.debug(f"{caller}{e}")


async def get_match_stats(page, caller):
    try:
        stats = {}
        non_nullable_stats = ['ball possession', 'total shots', 'shots_on_ target', 'corners kicks',
                        'yellow cards']
        nullable_stats = ['xg', 'big chances', 'xgot', 'shots off target', 'blocked shots',
                          'shots inside the box', 'shots outside the box', 'touches in opposition box',
                          'accurate through passes', 'offsides', 'free kicks', 'expected assists',
                          'throw ins', 'fouls', 'tackles', 'duels won', 'clearances', 'interceptions', 
                          'errors leading to shot', 'errors leading to goal', 'goals prevented']
        stats_rows = await page.locator(".container__livetable .container__detailInner .section .wcl-row_OFViZ").all()
        for row in stats_rows:
            try:
                category = await row.locator(".wcl-category_ITphf .wcl-category_7qsgP").first.text_content()
                if category:
                    for stat in non_nullable_stats:
                        if stat in category.lower():
                            home_val = await row.locator(".wcl-homeValue_-iJBW").first.text_content()
                            away_val = await row.locator(".wcl-awayValue_rQvxs").first.text_content()
                            home_stat = int(get_digit_string(home_val)) if get_digit_string(home_val).isdigit() else None
                            away_stat = int(get_digit_string(away_val)) if get_digit_string(away_val).isdigit() else None

                            if 'yellow' in stat and not home_stat and not away_stat:
                                home_stat, away_stat = 0, 0
                   
                            if not home_stat and not away_stat:
                                logger.debug(f"{caller} get_match_stats {stat} returns none")
                                return None
                            
                            stats["home_" + stat.replace(" ", "_")], stats["away_" + stat.replace(" ", "_")] = home_stat, away_stat
                    logger.debug(f"{caller} get_match_stats run successfully for required stats")

                    for stat in nullable_stats:
                        if stat in category.lower():
                            home_val = await row.locator(".wcl-homeValue_-iJBW").first.text_content()
                            away_val = await row.locator(".wcl-awayValue_rQvxs").first.text_content()
                            home_stat = int(get_digit_string(home_val)) if get_digit_string(home_val).isdigit() else None
                            away_stat = int(get_digit_string(away_val)) if get_digit_string(away_val).isdigit() else None
                            stats["home_" + stat.replace(" ", "_")], stats["away_" + stat.replace(" ", "_")] = home_stat, away_stat

                    logger.debug(f"{caller} get_match_stats run successfully for optional starts")
                
            except Exception as e:
                logger.debug(f"{caller} get_match_stats - {e}")
        return stats
    except Exception as e:
        logger.debug(f"f{caller} get_match_stats: {e}")
        return None
