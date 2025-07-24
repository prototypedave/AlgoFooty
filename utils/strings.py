import re

def split_score(score_text: str):
    scores = score_text.split("-")
    if len(scores) == 2:
        home_raw, away_raw = scores
        home_score = int(home_raw) if home_raw.isdigit() else None
        away_score = int(away_raw) if away_raw.isdigit() else None

        if home_score is not None and away_score is not None:
            return home_score, away_score

    return None, None

def get_digit_string(text: str) -> str:
    text = re.sub(r"[%()/]", "", text)
    return text.strip()

def split_value(value):
    s = str(value).zfill(2)  

    if len(s) == 2:
        return int(s[0]), int(s[1])
    elif len(s) == 3:
        if s.startswith('10'):
            return 10, int(s[2])
        else:
            return int(s[0]), int(s[1:])
    else:
        raise ValueError(f"Unexpected value format: {value}")


def split_string(input_str: str) -> tuple:
    parts = [p.strip() for p in input_str.split(" - ")]
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 3:
        return parts[0], parts[1] + " - " + parts[2]
    else:
        return parts[0], None
    
def extract_league_gameweek(s: str) -> int:
    s_lower = s.lower()

    if 'qualification' in s_lower or 'group' in s_lower:
        return None

    match = re.search(r'round\s+(\d+)', s_lower)
    if match:
        return int(match.group(1))

    return None