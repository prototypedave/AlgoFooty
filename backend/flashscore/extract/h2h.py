from extract.scrape_utils import split_value
from utils.logger import logger
import asyncio
import numpy as np


async def get_h2h(page, home, away, num, prev=False):
    try:
        buttons = await page.query_selector_all("button, [role='tab']")
        for i, btn in enumerate(buttons):
            text = (await btn.text_content() or "").strip()
            if text == "H2H":
                await btn.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await btn.click(timeout=5000)
                await page.wait_for_selector(".container__livetable .container__detailInner .h2h__section", timeout=7000)
                return await get_h2h_stats(page, home, away, num, prev) 
                
    except Exception as e:
        logger.debug(f"H2H: Error extracting stats: {e}")
    return None

async def get_h2h_stats(page, home, away, num, prev):
    stats = {}
    try:
        
        h2h_sections = await page.locator(".h2h__section").all()
        if len(h2h_sections) != 3:
            return None
        
        home_games = await h2h_sections[0].locator(".rows .h2h__row").all()
        if len(home_games) <= num:
            return None
        
        h2h_games = await h2h_sections[2].locator(".rows .h2h__row").all()
        if len(h2h_games) <= num:
            return None
        
        away_games = await h2h_sections[1].locator(".rows .h2h__row").all()
        if len(away_games) <= num:
            return None
        
        if prev:
            home_games = home_games[1:]
            away_games = away_games[1:]
            h2h_games = h2h_games[1:]
        else:
            home_games = home_games[:4]
            away_games = away_games[:4]
            h2h_games = h2h_games[:4]
        
        home_task = asyncio.create_task(get_head(home_games, home, 'home', stats))
        away_task = asyncio.create_task(get_head(away_games, away, 'away', stats))
        h2h_task = asyncio.create_task(get_head(h2h_games, home, 'h2h', stats))

        results = await asyncio.gather(home_task, away_task, h2h_task)
        for r in results:
            stats.update(r)

        return stats
    except Exception as e:
        logger.debug(f"H2H: get_h2h_stats : {e}")
        return None


async def get_head(games, team, prefix, h2h):
    team_score, team_conceded, at_home_score, at_away_score = [], [], [], []
    at_away_conceded, at_home_conceded = [], []
    team_over_lists = [[], [], [], []]  # lists to store over values [05, 15, 25, 35]
    game_over_lists = [[], [], [], []] # same
    other_lists = [[], [], [], [], [], []] # win, draw, lost, team cleansheet, btts, overall cleansheet
    
    at_home_team_over = [[], [], [], []] # 05, 15, 25, 35
    at_home_over = [[], [], [], []] # 05, 15, 25, 35
    at_home_other = [[], [], [], [], [], []] # win, draw, lost, team_cleansheet, btts overall cleansheet
    
    at_away_team_over = [[], [], [], []]
    at_away_over = [[], [], [], []]
    at_away_other = [[], [], [], [], [], []]

    num_games = len(games)

    for game in games:
        home = (await game.locator(".h2h__homeParticipant").text_content() or "").strip()
        away = (await game.locator(".h2h__awayParticipant").text_content() or "").strip()
        result = (await game.locator(".h2h__result").text_content() or "").strip()
        home_score, away_score = split_value(result)
        total_score = home_score + away_score
    
        if home == team:
            at_home_team_over = get_met_over(home_score, at_home_team_over)
            at_home_over = get_met_over(total_score, at_home_over)
            at_home_other = get_other_mets(home_score, away_score, at_home_other)
            at_home_score.append(home_score)
            at_home_conceded.append(away_score)

        if away == team:
            at_away_team_over = get_met_over(away_score, at_away_team_over)
            at_away_over = get_met_over(total_score, at_away_over)
            at_away_other = get_other_mets(away_score, home_score, at_away_other)
            at_away_score.append(away_score)
            at_away_conceded.append(home_score)

            tmp = home_score
            home_score = away_score
            away_score = tmp

        team_score.append(home_score)
        team_conceded.append(away_score)
        team_over_lists = get_met_over(home_score, team_over_lists)
        game_over_lists = get_met_over(total_score, game_over_lists)
        
        other_lists = get_other_mets(home_score, away_score, other_lists)

    ovr_lists = compute_metrics([team_over_lists, game_over_lists, other_lists], num_games)
    h2h = create_h2h_obj(prefix, ovr_lists, h2h)
    home_lists = [at_home_team_over, at_home_over, at_home_other]
    away_lists = [at_away_team_over, at_away_over,  at_away_other]
    h2h = merge_obj(prefix,  h2h, home_lists, away_lists, len(at_home_over), len(at_away_over))
    mean_score, roll_score = score_metrics(team_score, num_games)
    mean_conceded, roll_conceded = score_metrics(team_conceded, num_games)
    
    len_home = 1 if len(at_home_score) == 0 else len(at_home_score)
    len_away = 1 if len(at_away_score) == 0 else len(at_away_score)

    h2h[f'{prefix}_at_home_score'] = sum(at_home_score) / len_home
    h2h[f'{prefix}_at_home_conceded'] = sum(at_home_conceded) / len_home
    h2h[f'{prefix}_at_away_score'] = sum(at_away_score) / len_away
    h2h[f'{prefix}_at_away_conceded'] = sum(at_away_conceded) / len_away
    h2h[f'{prefix}_mean_score'] = mean_score
    h2h[f'{prefix}_roll_score'] = roll_score
    h2h[f'{prefix}_mean_conceded'] = mean_conceded
    h2h[f'{prefix}_roll_conceded'] = roll_conceded
    return h2h

def get_met_over(score, lists):
    over_05 = 1 if score >= 1 else 0
    over_15 = 1 if score >= 2 else 0
    over_25 = 1 if score >= 3 else 0
    over_35 = 1 if score >= 4 else 0
    
    for x, y in zip(lists, [over_05, over_15, over_25, over_35]):
        x.append(y)
    return lists


def get_other_mets(h_score, a_score, lists):
    winner = 1 if h_score > a_score else 0
    draw = 1 if h_score == a_score else 0
    lost = 1 if not winner and not draw else 0
    clean = 1 if h_score == 0 and a_score == 0 else 0
    team_clean = 1 if a_score == 0 else 0
    btts = 1 if h_score > 0 and a_score > 0 else 0

    for x, y in zip(lists, [winner, draw, lost, team_clean, btts, clean]): # ensure order of list is maintained
        x.append(y)
    return lists 


def get_average_mets(lists, num):
    avgs = []
    for l in lists:
        if len(l) == 0:
            avgs.append(0.0)
        else:
            avgs.append(sum(l) / len(l))  # use actual list length, not global num
    return avgs


def compute_metrics(lists, num):
    avg, roll = [], []
    for l in lists:
        avg += get_average_mets(l, num)
        roll += get_rolling_mean(l)
    return avg + roll


def get_rolling_mean(lists):
    rolls = []
    window_size = 3
    kernel = np.ones(window_size) / window_size
    for l in lists:
        arr = list(reversed(l))  # preserve "latest" logic without mutating original
        if len(arr) < window_size:
            rolls.append(sum(arr) / len(arr) if arr else 0.0)
        else:
            rolling = np.convolve(arr, kernel, mode='valid')
            rolls.append(rolling[-1].item())  # last = most recent
    return rolls


def score_metrics(scores, num):
    num = 1 if num == 0  else num
    avg = sum(scores) / num
    window_size = 3
    kernel = np.ones(window_size) / window_size
    rolling = np.convolve(scores, kernel, mode='valid')
    roll = rolling[-1].item()
    return avg, roll


def create_h2h_obj(prefix, lists, obj):
    keys = ['team_05', 'team_15', 'team_25', 'team_35', '05', '15', '25', '35',
            'win', 'draw', 'lost', 'team_clean_sheet', 'btts', 'game_clean_sheet',
            'team_roll_05', 'team_roll_15', 'team_roll_25', 'team_roll_35', 'roll_05', 
            'roll_15', 'roll_25', 'roll_35', 'roll_win', 'roll_draw', 'roll_lost', 
            'team_roll_clean_sheet', 'roll_btts', 'game_roll_clean_sheet',]
    for k, v in zip(keys, lists):
        obj[f"{prefix}_{k}"] = v
    return obj


def merge_obj(prefix, obj, home, away, len_home, len_away):
    home_mets, away_mets = [], []
    for l in home:
        home_mets += get_average_mets(l, len_home)

    for k in away:
        away_mets += get_average_mets(k, len_away)

    keys = ['team_05', 'team_15', 'team_25', 'team_35', '05', '15', '25', '35',
            'win', 'draw', 'lost', 'team_clean_sheet', 'btts', 'game_clean_sheet',]
    
    for k, i, l in zip(keys, home_mets, away_mets):
        obj[f"{prefix}_at_home_{k}"] = i
        obj[f'{prefix}_at_away_{k}'] = l
    return obj

