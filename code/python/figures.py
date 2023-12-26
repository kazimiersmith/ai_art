from set_globals import *

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

panel = pd.read_pickle(data / 'daily_data.pkl')
panel_both = pd.read_pickle(data / 'daily_data_both.pkl')
panel = panel[panel['date'] >= start_date].reset_index(drop = True)
panel_both = panel_both[panel_both['date'] >= start_date].reset_index(drop = True)

# Graph daily submissions to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['posts_organic', 'posts_ai'])
plt.xlabel('')
plt.ylabel('Daily submissions')
plt.savefig(figures / 'submissions.png')
plt.clf()

# Graph daily submissions per author to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['posts_per_author_organic', 'posts_per_author_ai'])
plt.xlabel('')
plt.ylabel('Daily submissions per author')
plt.savefig(figures / 'submissions_per_author.png')
plt.clf()

# Graph unique authors to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['authors_organic', 'authors_ai'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.savefig(figures / 'unique_authors.png')
plt.clf()

# Plot mean post score, excluding outliers from the API change protest
panel['api_protest'] = panel['date'].apply(lambda x: x in api_protest_dates)
panel[panel['api_protest'] == False].plot(x = 'date',
                                          y = ['post_score_organic',
                                               'post_score_ai'])
plt.xlabel('')
plt.ylabel('Mean post score')
plt.savefig(figures / 'mean_score.png')
plt.clf()

# Graph daily comments on r/Art and AI art subreddits
panel.plot(x = 'date', y = ['comments_organic', 'comments_ai'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.savefig(figures / 'comments.png')
plt.clf()

# Graph unique commenters to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['commenters_organic', 'commenters_ai'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters.png')
plt.clf()

# Graph daily comments per author
panel[panel['date'] >= datetime(2023, 1, 31)].plot(x = 'date', y = ['comments_per_author_organic', 'comments_per_author_ai'])
plt.xlabel('')
plt.ylabel('Daily comments per author')
plt.savefig(figures / 'comments_per_author.png')
plt.clf()

# Graph daily submissions to r/Art and AI art subreddits by authors who ever post on both
panel_both.plot(x = 'date', y = ['posts_organic', 'posts_ai'])
plt.xlabel('')
plt.ylabel('Daily submissions')
plt.savefig(figures / 'submissions_overlapping_authors.png')
plt.clf()

# Graph unique authors to r/Art and AI art subreddits, among authors who ever post on both
panel_both.plot(x = 'date', y = ['authors_organic', 'authors_ai'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.savefig(figures / 'unique_authors_overlapping_authors.png')
plt.clf()

# Graph daily comments on r/Art and AI art subreddits by commenters who ever comment on both
panel_both.plot(x = 'date', y = ['comments_organic', 'comments_ai'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.savefig(figures / 'comments_overlapping_commenters.png')
plt.clf()

# Graph unique commenters to r/Art and AI art subreddits, among commenters who ever comment on both
panel_both.plot(x = 'date', y = ['commenters_organic', 'commenters_ai'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters_overlapping_commenters.png')
plt.clf()

# Posts per author among authors who ever post on both
panel_both[panel_both['date'] >= all_subreddits_exist].plot(x = 'date',
                                                            y = ['posts_per_author_organic',
                                                                 'posts_per_author_ai'])
plt.xlabel('')
plt.ylabel('Posts per author')
plt.savefig(figures / 'posts_per_author_overlapping_authors.png')
plt.clf()

# Comments per author among commenters who ever comment on both
panel_both[panel_both['date'] >= all_subreddits_exist].plot(x = 'date',
                                                            y = ['comments_per_author_organic',
                                                                 'comments_per_author_ai'])
plt.xlabel('')
plt.ylabel('Comments per author')
plt.savefig(figures / 'comments_per_author_overlapping_commenters.png')
plt.clf()

# Scatter unique authors on AI art subreddits vs. r/Art (each point is a day)
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'authors_organic',
                                                          y = 'authors_ai')
plt.xlabel('Unique authors to r/Art')
plt.ylabel('Unique authors to AI art subreddits')
plt.savefig(figures / 'unique_authors_scatter.png')
plt.clf()

# Scatter posts on AI art subreddits vs. r/Art (each point is a day)
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'posts_organic',
                                                          y = 'posts_ai')
plt.xlabel('Posts on r/Art')
plt.ylabel('Posts on AI art subreddits')
plt.savefig(figures / 'submissions_scatter.png')
plt.clf()

# Scatter posts per author on AI art subreddits vs. r/Art (each point is a day)
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'posts_per_author_organic',
                                                          y = 'posts_per_author_ai')
plt.xlabel('Submissions per author to r/Art')
plt.ylabel('Submissions per author to AI art subreddits')
plt.savefig(figures / 'subs_per_author_scatter.png')
plt.clf()

# Scatter comment authors on AI art subreddits vs. r/Art
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'commenters_organic',
                                                          y = 'commenters_ai')
plt.xlabel('Unique commenters to r/Art')
plt.ylabel('Unique commenters to AI art subreddits')
plt.savefig(figures / 'unique_commenters_scatter.png')
plt.clf()

# Scatter comments on AI art subreddits vs. r/Art
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'comments_organic',
                                                          y = 'comments_ai')
plt.xlabel('Comments on r/Art')
plt.ylabel('Comments on AI art subreddits')
plt.savefig(figures / 'comments_scatter.png')
plt.clf()

# Scatter comments per author on AI art subreddits vs. r/Art
panel[panel['date'] >= all_subreddits_exist].plot.scatter(x = 'comments_per_author_organic',
                                                          y = 'comments_per_author_ai')
plt.xlabel('Comments per author to r/Art')
plt.ylabel('Comments per author to AI art subreddits')
plt.savefig(figures / 'comments_per_author_scatter.png')
