from pathlib import Path
from datetime import datetime

root = Path('~/research/ai_art').expanduser()
raw = Path('~/Dropbox/ai_art_raw').expanduser()
data = root / 'data'
figures = root / 'figures'

start_date = datetime(2021, 1, 1)

api_protest_dates = [datetime(2023, 6, 12),
                     datetime(2023, 6, 13),
                     datetime(2023, 6, 14)]

all_subreddits_exist = datetime(2022, 7, 23)

default_dpi = 300
