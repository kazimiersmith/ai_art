from set_globals import *

from pathlib import Path
import pandas as pd
from datetime import datetime

# Create daily panel
def create_daily_panel(posts, comments):
    posts_daily = posts.groupby('ai_subreddit').resample('D', on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    posts_daily = posts_daily.rename(columns = {'author': 'authors',
                                                'id': 'posts',
                                                'score': 'post_score'})
    posts_daily = posts_daily.unstack('ai_subreddit')
    posts_daily = posts_daily.reset_index()
    posts_daily = posts_daily.rename(columns = {False: 'organic', True: 'ai'})
    posts_daily.columns = ['_'.join(col).strip().lower() for col in posts_daily.columns.values]
    posts_daily = posts_daily.rename(columns = {'created_': 'date'})

    comments_daily = comments.groupby('ai_subreddit').resample('D', on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    comments_daily = comments_daily.rename(columns = {'author': 'commenters',
                                                      'id': 'comments',
                                                      'score': 'comment_score'})
    comments_daily = comments_daily.unstack('ai_subreddit')
    comments_daily = comments_daily.reset_index()
    comments_daily = comments_daily.rename(columns = {False: 'organic', True: 'ai'})
    comments_daily.columns = ['_'.join(col).strip().lower() for col in comments_daily.columns.values]
    comments_daily = comments_daily.rename(columns = {'created_': 'date'})

    return pd.merge(left = posts_daily,
                    right = comments_daily,
                    on = 'date',
                    how = 'inner')

posts_all = pd.read_pickle(data / 'posts.pkl')
comments_all = pd.read_pickle(data / 'comments.pkl')
posts_both = posts_all[posts_all['author_both'] == True].reset_index(drop = True)
comments_both = comments_all[comments_all['commenter_both'] == True].reset_index(drop = True)

# Panel with all data
daily_data = create_daily_panel(posts_all, comments_all)
daily_data['posts_per_author_organic'] = daily_data['posts_organic'] / daily_data['authors_organic']
daily_data['comments_per_author_organic'] = daily_data['comments_organic'] / daily_data['commenters_organic']
daily_data['posts_per_author_ai'] = daily_data['posts_ai'] / daily_data['authors_ai']
daily_data['comments_per_author_ai'] = daily_data['comments_ai'] / daily_data['commenters_ai']
daily_data['comments_per_post_organic'] = daily_data['comments_organic'] / daily_data['posts_organic']
daily_data['comments_per_post_ai'] = daily_data['comments_ai'] / daily_data['posts_ai']
daily_data.to_pickle(data / 'daily_data.pkl')

# Panel with only authors/commenters in both AI subreddits and r/Art
daily_data_both = create_daily_panel(posts_both, comments_both)
daily_data_both['posts_per_author_organic'] = daily_data_both['posts_organic'] / daily_data_both['authors_organic']
daily_data_both['comments_per_author_organic'] = daily_data_both['comments_organic'] / daily_data_both['commenters_organic']
daily_data_both['posts_per_author_ai'] = daily_data_both['posts_ai'] / daily_data_both['authors_ai']
daily_data_both['comments_per_author_ai'] = daily_data_both['comments_ai'] / daily_data_both['commenters_ai']
daily_data_both['comments_per_post_organic'] = daily_data_both['comments_organic'] / daily_data_both['posts_organic']
daily_data_both['comments_per_post_ai'] = daily_data_both['comments_ai'] / daily_data_both['posts_ai']
daily_data_both.to_pickle(data / 'daily_data_both.pkl')
