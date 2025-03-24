from set_globals import *

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Create commenter-day panel, only using commenters who ever comment
# in both AI and organic subreddits
posts_all = pd.read_pickle(data / 'posts.pkl')
comments_all = pd.read_pickle(data / 'comments.pkl')
comments_both = comments_all[comments_all['commenter_both'] == True].reset_index(drop = True)
comments_both = comments_both[comments_both['author'] != '[deleted]'].reset_index(drop = True)

commenter_panel = comments_both.groupby(['author', 'ai_subreddit']).resample('D', on = 'created').agg({
    'id': 'count', # Assuming comments aren't duplicated
    'score': 'mean'})

commenter_panel = commenter_panel.rename(columns = {'id': 'comments'})
commenter_panel = commenter_panel.unstack('ai_subreddit')
commenter_panel = commenter_panel.reset_index()
commenter_panel = commenter_panel.rename(columns = {False: 'organic', True: 'ai'})
commenter_panel.columns = ['_'.join(col).strip().lower() for col in commenter_panel.columns.values]
commenter_panel = commenter_panel.rename(columns = {'created_': 'date',
                                                    'author_': 'author'})

max_date = commenter_panel['date'].max()
all_dates = pd.DataFrame({'date': pd.date_range(start_date, max_date, freq = 'D')})
all_commenters = pd.DataFrame({'author': comments_both['author'].unique()})
commenters_dates = pd.merge(all_dates, all_commenters, how = 'cross')
commenter_panel = pd.merge(left = commenters_dates,
                           right = commenter_panel,
                           how = 'left',
                           on = ['date', 'author'])

commenter_panel = commenter_panel.fillna({'comments_organic': 0,
                                          'comments_ai': 0})

commenter_panel['cum_comments_ai'] = commenter_panel.groupby('author')['comments_ai'].cumsum()
commenter_panel['cum_comments_organic'] = commenter_panel.groupby('author')['comments_organic'].cumsum()
commenter_panel['has_commented_ai'] = commenter_panel['cum_comments_ai'] > 0
commenter_panel['has_commented_organic'] = commenter_panel['cum_comments_organic'] > 0

commenter_panel['diff_comments'] = commenter_panel['comments_organic'] - commenter_panel['comments_ai']

# Sum all future comments
commenter_panel['future_comments_ai'] = commenter_panel.groupby('author')['comments_ai'].transform(lambda x: x[::-1].cumsum()[::-1])
commenter_panel['future_comments_organic'] = commenter_panel.groupby('author')['comments_organic'].transform(lambda x: x[::-1].cumsum()[::-1])
commenter_panel['has_future_comments_ai'] = commenter_panel['future_comments_ai'] > 0
commenter_panel['has_future_comments_organic'] = commenter_panel['future_comments_organic'] > 0

commenter_panel.to_pickle(data / 'commenter_panel.pkl')
