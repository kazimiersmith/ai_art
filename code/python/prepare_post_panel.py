from set_globals import *

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Create panel with given frequency
def create_panel(posts, comments, freq):
    posts_freq = posts.groupby('ai_subreddit').resample(freq, on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    posts_freq = posts_freq.rename(columns = {'author': 'authors',
                                                'id': 'posts',
                                                'score': 'post_score'})
    posts_freq = posts_freq.unstack('ai_subreddit')
    posts_freq = posts_freq.reset_index()
    posts_freq = posts_freq.rename(columns = {False: 'organic', True: 'ai'})
    posts_freq.columns = ['_'.join(col).strip().lower() for col in posts_freq.columns.values]
    posts_freq = posts_freq.rename(columns = {'created_': 'date'})

    comments_freq = comments.groupby('ai_subreddit').resample(freq, on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    comments_freq = comments_freq.rename(columns = {'author': 'commenters',
                                                      'id': 'comments',
                                                      'score': 'comment_score'})
    comments_freq = comments_freq.unstack('ai_subreddit')
    comments_freq = comments_freq.reset_index()
    comments_freq = comments_freq.rename(columns = {False: 'organic', True: 'ai'})
    comments_freq.columns = ['_'.join(col).strip().lower() for col in comments_freq.columns.values]
    comments_freq = comments_freq.rename(columns = {'created_': 'date'})

    return pd.merge(left = posts_freq,
                    right = comments_freq,
                    on = 'date',
                    how = 'inner')

posts_all = pd.read_pickle(data / 'posts.pkl')
comments_all = pd.read_pickle(data / 'comments.pkl')
posts_both = posts_all[posts_all['author_both'] == True].reset_index(drop = True)
comments_both = comments_all[comments_all['commenter_both'] == True].reset_index(drop = True)

# Panel with all data
freq_data = create_panel(posts_all, comments_all, 'W')
freq_data['posts_per_author_organic'] = freq_data['posts_organic'] / freq_data['authors_organic']
freq_data['comments_per_author_organic'] = freq_data['comments_organic'] / freq_data['commenters_organic']
freq_data['posts_per_author_ai'] = freq_data['posts_ai'] / freq_data['authors_ai']
freq_data['comments_per_author_ai'] = freq_data['comments_ai'] / freq_data['commenters_ai']
freq_data['comments_per_post_organic'] = freq_data['comments_organic'] / freq_data['posts_organic']
freq_data['comments_per_post_ai'] = freq_data['comments_ai'] / freq_data['posts_ai']
freq_data['day_of_week'] = freq_data['date'].dt.weekday
freq_data = freq_data.replace([np.inf, -np.inf], np.nan)
freq_data.to_pickle(data / 'freq_data.pkl')

# Panel with only authors/commenters in both AI subreddits and r/Art
freq_data_both = create_panel(posts_both, comments_both, 'W')
freq_data_both['posts_per_author_organic'] = freq_data_both['posts_organic'] / freq_data_both['authors_organic']
freq_data_both['comments_per_author_organic'] = freq_data_both['comments_organic'] / freq_data_both['commenters_organic']
freq_data_both['posts_per_author_ai'] = freq_data_both['posts_ai'] / freq_data_both['authors_ai']
freq_data_both['comments_per_author_ai'] = freq_data_both['comments_ai'] / freq_data_both['commenters_ai']
freq_data_both['comments_per_post_organic'] = freq_data_both['comments_organic'] / freq_data_both['posts_organic']
freq_data_both['comments_per_post_ai'] = freq_data_both['comments_ai'] / freq_data_both['posts_ai']
freq_data_both['day_of_week'] = freq_data_both['date'].dt.weekday
freq_data_both = freq_data_both.replace([np.inf, -np.inf], np.nan)
freq_data_both.to_pickle(data / 'freq_data_both.pkl')
