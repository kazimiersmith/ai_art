from set_globals import *

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Start graphs after all AI art subreddits were created, and exclude the dates of the
# Reddit API change protest. The latter dates have zero posts for some subreddits
panel = pd.read_pickle(data / 'freq_data.pkl')
panel = panel[panel['date'] >= start_date].reset_index(drop = True)
panel['api_protest'] = panel['date'].apply(lambda x: x in api_protest_dates)

panel_both = pd.read_pickle(data / 'freq_data_both.pkl')
panel_both = panel_both[panel_both['date'] >= start_date].reset_index(drop = True)
panel_both['api_protest'] = panel_both['date'].apply(lambda x: x in api_protest_dates)

commenter_panel = pd.read_pickle(data / 'commenter_panel.pkl')
author_panel = pd.read_pickle(data / 'author_panel.pkl')

# Graph daily submissions to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['posts_organic', 'posts_ai'])
plt.xlabel('')
plt.ylabel('Daily posts')
plt.legend(['Organic', 'AI'])
plt.savefig(figures / 'posts.png', dpi = default_dpi)
plt.close()

# Graph daily posts per author to r/Art and AI art subreddits
panel[panel['date'] >= all_subreddits_exist].plot(x = 'date', y = ['posts_per_author_organic', 'posts_per_author_ai'])
plt.xlabel('')
plt.ylabel('Daily posts per author')
plt.legend(['Organic', 'AI'])
plt.savefig(figures / 'posts_per_author.png', dpi = default_dpi)
plt.close()

# Graph unique authors to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['authors_organic', 'authors_ai'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.legend(['Organic', 'AI'])
plt.savefig(figures / 'unique_authors.png', dpi = default_dpi)
plt.close()

# Plot mean post score
panel.plot(x = 'date',y = ['post_score_organic', 'post_score_ai'])
plt.xlabel('')
plt.ylabel('Mean post score')
plt.savefig(figures / 'mean_score.png', dpi = default_dpi)
plt.close()

# Graph daily comments on r/Art and AI art subreddits
panel.plot(x = 'date', y = ['comments_organic', 'comments_ai'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.legend(['Organic', 'AI'])
plt.savefig(figures / 'comments.png', dpi = default_dpi)
plt.close()

# Graph unique commenters to r/Art and AI art subreddits
panel.plot(x = 'date', y = ['commenters_organic', 'commenters_ai'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters.png', dpi = default_dpi)
plt.close()

# Graph daily comments per author
panel.plot(x = 'date', y = ['comments_per_author_organic', 'comments_per_author_ai'])
plt.xlabel('')
plt.ylabel('Daily comments per author')
plt.savefig(figures / 'comments_per_author.png', dpi = default_dpi)
plt.close()

# Graph daily comments per post
panel.plot(x = 'date', y = ['comments_per_post_organic', 'comments_per_post_ai'])
plt.xlabel('')
plt.ylabel('Daily comments per post')
plt.savefig(figures / 'comments_per_post.png', dpi = default_dpi)

# Graph daily submissions to r/Art and AI art subreddits by authors who ever post on both
panel_both.plot(x = 'date', y = ['posts_organic', 'posts_ai'])
plt.xlabel('')
plt.ylabel('Daily submissions')
plt.savefig(figures / 'submissions_overlapping_authors.png', dpi = default_dpi)
plt.close()

# Graph unique authors to r/Art and AI art subreddits, among authors who ever post on both
panel_both.plot(x = 'date', y = ['authors_organic', 'authors_ai'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.savefig(figures / 'unique_authors_overlapping_authors.png', dpi = default_dpi)
plt.close()

# Graph daily comments on r/Art and AI art subreddits by commenters who ever comment on both
panel_both.plot(x = 'date', y = ['comments_organic', 'comments_ai'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.savefig(figures / 'comments_overlapping_commenters.png', dpi = default_dpi)
plt.close()

# Graph unique commenters to r/Art and AI art subreddits, among commenters who ever comment on both
panel_both.plot(x = 'date', y = ['commenters_organic', 'commenters_ai'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters_overlapping_commenters.png', dpi = default_dpi)
plt.close()

# Posts per author among authors who ever post on both
panel_both.plot(x = 'date', y = ['posts_per_author_organic', 'posts_per_author_ai'])
plt.xlabel('')
plt.ylabel('Posts per author')
plt.savefig(figures / 'posts_per_author_overlapping_authors.png', dpi = default_dpi)
plt.close()

# Comments per author among commenters who ever comment on both
panel_both.plot(x = 'date',
                y = ['comments_per_author_organic',
                     'comments_per_author_ai'])
plt.xlabel('')
plt.ylabel('Comments per author')
plt.savefig(figures / 'comments_per_author_overlapping_commenters.png', dpi = default_dpi)
plt.close()

# Comments per post among commenters who ever comment on both
# NOTE: this figure isn't really representing anything because of how panel_both
# is created
panel_both.plot(x = 'date', y = ['comments_per_post_organic', 'comments_per_post_ai'])
plt.xlabel('')
plt.ylabel('Comments per post')
plt.savefig(figures / 'comments_per_post_overlapping_commenters.png', dpi = default_dpi)
plt.close()

# Scatter unique authors on AI art subreddits vs. r/Art (each point is a day)
panel.plot.scatter(x = 'authors_organic',
                   y = 'authors_ai')
plt.xlabel('Unique authors to r/Art')
plt.ylabel('Unique authors to AI art subreddits')
plt.savefig(figures / 'unique_authors_scatter.png', dpi = default_dpi)
plt.close()

# Scatter posts on AI art subreddits vs. r/Art (each point is a day)
panel.plot.scatter(x = 'posts_organic',
                   y = 'posts_ai')
plt.xlabel('Posts on r/Art')
plt.ylabel('Posts on AI art subreddits')
plt.savefig(figures / 'submissions_scatter.png', dpi = default_dpi)
plt.close()

# Scatter posts per author on AI art subreddits vs. r/Art (each point is a day)
panel.plot.scatter(x = 'posts_per_author_organic',
                   y = 'posts_per_author_ai')
plt.xlabel('Submissions per author to r/Art')
plt.ylabel('Submissions per author to AI art subreddits')
plt.savefig(figures / 'subs_per_author_scatter.png', dpi = default_dpi)
plt.close()

# Scatter comment authors on AI art subreddits vs. r/Art
panel.plot.scatter(x = 'commenters_organic',
                   y = 'commenters_ai')
plt.xlabel('Unique commenters to r/Art')
plt.ylabel('Unique commenters to AI art subreddits')
plt.savefig(figures / 'unique_commenters_scatter.png', dpi = default_dpi)
plt.close()

# Scatter comments on AI art subreddits vs. r/Art
panel.plot.scatter(x = 'comments_organic',
                   y = 'comments_ai')
plt.xlabel('Comments on r/Art')
plt.ylabel('Comments on AI art subreddits')
plt.savefig(figures / 'comments_scatter.png', dpi = default_dpi)
plt.close()

# Scatter comments per author on AI art subreddits vs. r/Art
panel.plot.scatter(x = 'comments_per_author_organic',
                   y = 'comments_per_author_ai')
plt.xlabel('Comments per author to r/Art')
plt.ylabel('Comments per author to AI art subreddits')
plt.savefig(figures / 'comments_per_author_scatter.png', dpi = default_dpi)
plt.close()

# Scatter comments per post on AI art subreddits vs. r/Art
panel.plot.scatter(x = 'comments_per_post_organic',
                   y = 'comments_per_post_ai')
plt.xlabel('Comments per post on r/Art')
plt.ylabel('Comments per post on AI art subreddits')
plt.savefig(figures / 'comments_per_post_scatter.png', dpi = default_dpi)
plt.close()

# Plot number of commenters who have ever commented on AI and organic subreddits
commenter_panel.groupby('date').sum().plot(y = ['has_commented_organic',
                                                 'has_commented_ai'])
plt.xlabel('')
plt.ylabel('Number of commenters')
plt.savefig(figures / 'commenters_ever_commented.png', dpi = default_dpi)
plt.close()

commenter_panel.groupby('date').mean(numeric_only = True).plot(y = ['comments_organic',
                                                                      'comments_ai'])
plt.xlabel('')
plt.ylabel('Average comments per commenter')
plt.savefig(figures / 'comments_per_commenter.png', dpi = default_dpi)
plt.close()

commenter_panel.groupby('date').mean(numeric_only = True).plot(y = 'diff_comments')
plt.xlabel('')
plt.ylabel('Average difference in comments')
plt.savefig(figures / 'comments_diff.png', dpi = default_dpi)
plt.close()

commenter_panel.groupby('date').sum().plot(y = ['has_future_comments_organic',
                                                'has_future_comments_ai'])
plt.xlabel('')
plt.ylabel('Number of commenters')
plt.savefig(figures / 'commenters_future_comments.png', dpi = default_dpi)
plt.close()

commenter_panel.groupby('date').mean(numeric_only = True).plot(y = ['future_comments_organic',
                                                                    'future_comments_ai'])
plt.xlabel('')
plt.ylabel('Average future comments')
plt.savefig(figures / 'future_comments.png', dpi = default_dpi)
plt.close()

# Plot number of authors who have ever posted on AI and organic subreddits
author_panel.groupby('date').sum().plot(y = ['has_posted_organic',
                                                 'has_posted_ai'])
plt.xlabel('')
plt.ylabel('Number of authors')
plt.savefig(figures / 'authors_ever_posted.png', dpi = default_dpi)
plt.close()

author_panel.groupby('date').mean(numeric_only = True).plot(y = ['posts_organic',
                                                                      'posts_ai'])
plt.xlabel('')
plt.ylabel('Average posts per author (author panel)')
plt.savefig(figures / 'posts_per_author_author_panel.png', dpi = default_dpi)
plt.close()

author_panel.groupby('date').mean(numeric_only = True).plot(y = 'diff_posts')
plt.xlabel('')
plt.ylabel('Average difference in posts')
plt.savefig(figures / 'posts_diff.png', dpi = default_dpi)
plt.close()

author_panel.groupby('date').sum().plot(y = ['has_future_posts_organic',
                                                'has_future_posts_ai'])
plt.xlabel('')
plt.ylabel('Number of authors')
plt.savefig(figures / 'authors_future_posts.png', dpi = default_dpi)
plt.close()

author_panel.groupby('date').mean(numeric_only = True).plot(y = ['future_posts_organic',
                                                                    'future_posts_ai'])
plt.xlabel('')
plt.ylabel('Average future posts')
plt.savefig(figures / 'future_posts.png', dpi = default_dpi)
plt.close()

