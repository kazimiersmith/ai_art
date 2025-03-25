from set_globals import *

from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np

# Create panel with given frequency
def create_panel(posts, comments, freq):
    posts_freq = posts.groupby('subreddit').resample(freq, on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    posts_freq = posts_freq.rename(columns = {'author': 'authors',
                                                'id': 'posts',
                                                'score': 'post_score'})
    posts_freq = posts_freq.unstack('subreddit')
    posts_freq = posts_freq.reset_index()
    posts_freq = posts_freq.rename(columns = {False: 'organic', True: 'ai'})
    posts_freq.columns = ['_'.join(col).strip().lower() for col in posts_freq.columns.values]
    posts_freq = posts_freq.rename(columns = {'created_': 'date'})

    comments_freq = comments.groupby('subreddit').resample(freq, on = 'created').agg({
        'score': 'mean',
        'author': 'nunique',
        'id': 'nunique'})
    comments_freq = comments_freq.rename(columns = {'author': 'commenters',
                                                      'id': 'comments',
                                                      'score': 'comment_score'})
    comments_freq = comments_freq.unstack('subreddit')
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

# Panel with only authors/commenters in both AI subreddits and r/Art
freq_data_both = create_panel(posts_both, comments_both, 'W')

for s in ['art', 'aiart', 'midjourney', 'stablediffusion', 'dalle2']:
    freq_data[f'posts_per_author_{s}'] = freq_data[f'posts_{s}'] / freq_data[f'authors_{s}']
    freq_data[f'comments_per_author_{s}'] = freq_data[f'comments_{s}'] / freq_data[f'commenters_{s}']
    freq_data[f'comments_per_post_{s}'] = freq_data[f'comments_{s}'] / freq_data[f'posts_{s}']
    freq_data = freq_data.replace([np.inf, -np.inf], np.nan)
    freq_data.to_pickle(data / 'freq_data_indiv.pkl')

    freq_data_both[f'posts_per_author_{s}'] = freq_data_both[f'posts_{s}'] / freq_data_both[f'authors_{s}']
    freq_data_both[f'comments_per_author_{s}'] = freq_data_both[f'comments_{s}'] / freq_data_both[f'commenters_{s}']
    freq_data_both[f'comments_per_post_{s}'] = freq_data_both[f'comments_{s}'] / freq_data_both[f'posts_{s}']
    freq_data_both = freq_data_both.replace([np.inf, -np.inf], np.nan)
    freq_data_both.to_pickle(data / 'freq_data_both_indiv.pkl')

