from set_globals import *

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Create author-day panel;
# random sample for now so it runs faster
posts_all = pd.read_pickle(data / 'posts.pkl')
posts = posts_all[posts_all['author'] != '[deleted]'].sample(frac = 0.01).reset_index(drop = True)

author_panel = posts.groupby(['author', 'ai_subreddit']).resample('W', on = 'created').agg({
    'id': 'count', # Assuming posts aren't duplicated
    'score': 'mean'})

author_panel = author_panel.rename(columns = {'id': 'posts'})
author_panel = author_panel.unstack('ai_subreddit')
author_panel = author_panel.reset_index()
author_panel = author_panel.rename(columns = {False: 'organic', True: 'ai'})
author_panel.columns = ['_'.join(col).strip().lower() for col in author_panel.columns.values]
author_panel = author_panel.rename(columns = {'created_': 'date',
                                                    'author_': 'author'})

max_date = author_panel['date'].max()
all_dates = pd.DataFrame({'date': pd.date_range(start_date, max_date, freq = 'W')})
all_authors = pd.DataFrame({'author': posts['author'].unique()})
authors_dates = pd.merge(all_dates, all_authors, how = 'cross')
author_panel = pd.merge(left = authors_dates,
                           right = author_panel,
                           how = 'left',
                           on = ['date', 'author'])

author_panel = author_panel.fillna({'posts_organic': 0,
                                          'posts_ai': 0})

author_panel = author_panel.sort_values(by = ['author', 'date'])

author_panel['cum_posts_ai'] = author_panel.groupby('author')['posts_ai'].cumsum()
author_panel['cum_posts_organic'] = author_panel.groupby('author')['posts_organic'].cumsum()
author_panel['has_posted_ai'] = author_panel['cum_posts_ai'] > 0
author_panel['has_posted_organic'] = author_panel['cum_posts_organic'] > 0

author_panel['diff_posts'] = author_panel['posts_organic'] - author_panel['posts_ai']

# Sum all future posts
author_panel['future_posts_ai'] = author_panel.groupby('author')['posts_ai'].transform(lambda x: x[::-1].cumsum()[::-1])
author_panel['future_posts_organic'] = author_panel.groupby('author')['posts_organic'].transform(lambda x: x[::-1].cumsum()[::-1])
author_panel['has_future_posts_ai'] = author_panel['future_posts_ai'] > 0
author_panel['has_future_posts_organic'] = author_panel['future_posts_organic'] > 0

# Whether the author starts posting on AI art subreddits this period
# after having posted on r/Art in the past
author_panel['has_posted_ai_prev'] = author_panel['has_posted_ai'].shift(1)
author_panel['has_posted_organic_prev'] = author_panel['has_posted_organic'].shift(1)

author_panel['first_post_ai'] = (author_panel['has_posted_ai'] == True) & (author_panel['has_posted_ai_prev'] == False)
author_panel['first_post_organic'] = (author_panel['has_posted_organic'] == True) & (author_panel['has_posted_organic_prev'] == False)

author_panel['adopted_ai'] = (author_panel['first_post_ai'] == True) & (author_panel['has_posted_organic'] == True)

author_panel.to_pickle(data / 'author_panel.pkl')

