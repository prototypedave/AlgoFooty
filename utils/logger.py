import logging
import colorlog

# Define ASCI colors
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"  
GREEN = "\033[32m" 
PURPLE = "\033[0;35m"   
WHITE = "\033[0;35m"     

# Default tags
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'blue',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Optional tags
tag_colors = {
    "DB:": ORANGE,
    "SCRAPE:": GREEN,
    "FLASHSCORE": PURPLE,
    "GAME": WHITE
}

# Assign color based on the tags
class TagColorFilter(logging.Filter):
    def filter(self, record):
        for tag, color in tag_colors.items():
            if record.msg.startswith(tag):
                tag_colored = f"{color}{tag}{color}"
                rest = record.msg[len(tag):].lstrip()
                record.msg = f"{tag_colored} {rest}"
                break
        return True

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors=log_colors,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.addFilter(TagColorFilter())

if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(handler)