from set_globals import *

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

subs = pd.read_pickle(data / 'subs.pkl')

# Graph daily submissions to r/Art and AI art subreddits
subs_daily = subs.groupby('ai_subreddit').resample('D', on = 'created').agg('count').unstack('ai_subreddit')['ai_subreddit']
subs_daily = subs_daily.reset_index()
subs_daily = subs_daily.rename(columns = {False: 'Organic', True: 'AI'})
subs_daily.columns.name = None
subs_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily submissions')
plt.savefig(figures / 'submissions.png')
plt.clf()

# Graph daily submissions per author to r/Art and AI art subreddits
subs_daily = subs.groupby('ai_subreddit').resample('D', on = 'created').agg({
    'author': 'nunique',
    'id': 'count'}).unstack('ai_subreddit')
subs_daily = subs_daily.reset_index()
subs_daily = subs_daily.rename(columns = {False: 'Organic', True: 'AI'})
subs_daily.columns.name = None
subs_daily.columns = ['_'.join(col).strip() for col in subs_daily.columns.values]
subs_daily = subs_daily.rename(columns = {'created_': 'created'})
subs_daily['subs_per_author_Organic'] = subs_daily['id_Organic'] / subs_daily['author_Organic']
subs_daily['subs_per_author_AI'] = subs_daily['id_AI'] / subs_daily['author_AI']
subs_daily.plot(x = 'created', y = ['subs_per_author_Organic', 'subs_per_author_AI'])
plt.xlabel('')
plt.ylabel('Weekly submissions per author')
plt.savefig(figures / 'submissions_per_author.png')
plt.clf()

# Graph unique authors to r/Art and AI art subreddits
authors_daily = subs.groupby('ai_subreddit').resample('D', on = 'created')['author'].nunique().unstack('ai_subreddit')
authors_daily = authors_daily.reset_index()
authors_daily = authors_daily.rename(columns = {False: 'Organic', True: 'AI'})
authors_daily.columns.name = None
authors_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.savefig(figures / 'unique_authors.png')
plt.clf()

score_daily = subs.groupby('ai_subreddit').resample('D', on = 'created')['score'].agg(['mean', 'median']).unstack('ai_subreddit')
# A couple of days have no or very few posts; maybe an issue with Pushshift
score_daily = score_daily[score_daily['mean'] <= 600]
score_daily = score_daily.reset_index()
score_daily = score_daily.rename(columns = {False: 'Organic', True: 'AI'})
score_daily.columns.name = None

# Flatten column names
score_daily.columns = ['_'.join(col).strip() for col in score_daily.columns.values]
score_daily = score_daily.rename(columns = {'created_': 'created'})

score_daily.plot(x = 'created', y = ['mean_Organic', 'mean_AI'])
plt.xlabel('')
plt.ylabel('Mean post score')
plt.savefig(figures / 'mean_score.png')
plt.clf()

score_daily.plot(x = 'created', y = ['median_Organic', 'median_AI'])
plt.xlabel('')
plt.ylabel('Median post score')
plt.savefig(figures / 'median_score.png')
plt.clf()

comments = pd.read_pickle(data / 'comments.pkl')

# Graph daily comments on r/Art and AI art subreddits
comments_daily = comments.groupby('ai_subreddit').resample('D', on = 'created').agg('count').unstack('ai_subreddit')['ai_subreddit']
comments_daily = comments_daily.reset_index()
comments_daily = comments_daily.rename(columns = {False: 'Organic', True: 'AI'})
comments_daily.columns.name = None
comments_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.savefig(figures / 'comments.png')
plt.clf()

# Graph unique commenters to r/Art and AI art subreddits
commenters_daily = comments.groupby('ai_subreddit').resample('D', on = 'created')['author'].nunique().unstack('ai_subreddit')
commenters_daily = commenters_daily.reset_index()
commenters_daily = commenters_daily.rename(columns = {False: 'Organic', True: 'AI'})
commenters_daily.columns.name = None
commenters_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters.png')
plt.clf()

# Authors who ever post on both subreddits
ai_authors = set(subs[subs['ai_subreddit'] == True]['author'])
art_authors = set(subs[subs['ai_subreddit'] == False]['author'])
authors_both = ai_authors & art_authors - set(['[deleted]'])

subs_both = subs[subs['author'].isin(authors_both)].reset_index()

# Graph daily submissions to r/Art and AI art subreddits by authors who ever post on both
subs_both_daily = subs_both.groupby('ai_subreddit').resample('D', on = 'created').agg('count').unstack('ai_subreddit')['ai_subreddit']
subs_both_daily = subs_both_daily.reset_index()
subs_both_daily = subs_both_daily.rename(columns = {False: 'Organic', True: 'AI'})
subs_both_daily.columns.name = None
subs_both_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily submissions')
plt.savefig(figures / 'submissions_overlapping_authors.png')
plt.clf()

# Graph unique authors to r/Art and AI art subreddits, among authors who ever post on both
authors_both_daily = subs_both.groupby('ai_subreddit').resample('D', on = 'created')['author'].nunique().unstack('ai_subreddit')
authors_both_daily = authors_both_daily.reset_index()
authors_both_daily = authors_both_daily.rename(columns = {False: 'Organic', True: 'AI'})
authors_both_daily.columns.name = None
authors_both_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily unique post authors')
plt.savefig(figures / 'unique_authors_overlapping_authors.png')
plt.clf()

ai_commenters = set(comments[comments['ai_subreddit'] == True]['author'])
art_commenters = set(comments[comments['ai_subreddit'] == False]['author'])
commenters_both = ai_commenters & art_commenters - set(['[deleted]'])

comments_both = comments[comments['author'].isin(commenters_both)].reset_index()

# Graph daily comments on r/Art and AI art subreddits by commenters who ever comment on both
comments_both_daily = comments_both.groupby('ai_subreddit').resample('D', on = 'created').agg('count').unstack('ai_subreddit')['ai_subreddit']
comments_both_daily = comments_both_daily.reset_index()
comments_both_daily = comments_both_daily.rename(columns = {False: 'Organic', True: 'AI'})
comments_both_daily.columns.name = None
comments_both_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily comments')
plt.savefig(figures / 'comments_overlapping_commenters.png')
plt.clf()

# Graph unique commenters to r/Art and AI art subreddits, among commenters who ever comment on both
commenters_both_daily = comments_both.groupby('ai_subreddit').resample('D', on = 'created')['author'].nunique().unstack('ai_subreddit')
commenters_both_daily = commenters_both_daily.reset_index()
commenters_both_daily = commenters_both_daily.rename(columns = {False: 'Organic', True: 'AI'})
commenters_both_daily.columns.name = None
commenters_both_daily.plot(x = 'created', y = ['Organic', 'AI'])
plt.xlabel('')
plt.ylabel('Daily unique commenters')
plt.savefig(figures / 'unique_commenters_overlapping_commenters.png')
plt.clf()

subs_daily = subs_both.groupby('ai_subreddit').resample('D', on = 'created').agg({
    'author': 'nunique',
    'id': 'count'}).unstack('ai_subreddit')
subs_daily = subs_daily.reset_index()
subs_daily = subs_daily.rename(columns = {False: 'Organic', True: 'AI'})
subs_daily.columns.name = None
subs_daily.columns = ['_'.join(col).strip() for col in subs_daily.columns.values]
subs_daily = subs_daily.rename(columns = {'created_': 'created'})
subs_daily['subs_per_author_Organic'] = subs_daily['id_Organic'] / subs_daily['author_Organic']
subs_daily['subs_per_author_AI'] = subs_daily['id_AI'] / subs_daily['author_AI']
subs_daily.plot(x = 'created', y = ['subs_per_author_Organic', 'subs_per_author_AI'])
plt.xlabel('')
plt.ylabel('Weekly submissions per author')
plt.savefig(figures / 'subs_per_author_overlapping_authors.png')
plt.clf()

# Restrict to dates after all subreddits were created
subs_daily = subs.groupby('ai_subreddit').resample('D', on = 'created').agg({
    'author': 'nunique',
    'id': 'count'}).unstack('ai_subreddit')
subs_daily = subs_daily.reset_index()
subs_daily = subs_daily.rename(columns = {False: 'Organic', True: 'AI'})
subs_daily.columns.name = None
subs_daily.columns = ['_'.join(col).strip() for col in subs_daily.columns.values]
subs_daily = subs_daily.rename(columns = {'created_': 'created'})
subs_daily['subs_per_author_Organic'] = subs_daily['id_Organic'] / subs_daily['author_Organic']
subs_daily['subs_per_author_AI'] = subs_daily['id_AI'] / subs_daily['author_AI']

subs_daily = subs_daily[subs_daily['created'] >= datetime(2022, 7, 23)]
plt.scatter(x = subs_daily['author_Organic'], y = subs_daily['author_AI'])
plt.xlabel('Unique authors to r/Art')
plt.ylabel('Unique authors to AI art subreddits')
plt.savefig(figures / 'unique_authors_scatter.png')
plt.clf()

plt.scatter(x = subs_daily['id_Organic'], y = subs_daily['id_AI'])
plt.xlabel('Submissions to r/Art')
plt.ylabel('Submissions to AI art subreddits')
plt.savefig(figures / 'submissions_scatter.png')
plt.clf()

plt.scatter(x = subs_daily['subs_per_author_Organic'], y = subs_daily['subs_per_author_AI'])
plt.xlabel('Submissions per author to r/Art')
plt.ylabel('Submissions per author to AI art subreddits')
plt.savefig(figures / 'subs_per_author_scatter.png')
plt.clf()

# Scatter comments on AI art subreddits vs. r/Art
comments_daily = comments.groupby('ai_subreddit').resample('D', on = 'created').agg({
    'author': 'nunique',
    'id': 'count'}).unstack('ai_subreddit')
comments_daily = comments_daily.reset_index()
comments_daily = comments_daily.rename(columns = {False: 'Organic', True: 'AI'})
comments_daily.columns.name = None
comments_daily.columns = ['_'.join(col).strip() for col in comments_daily.columns.values]
comments_daily = comments_daily.rename(columns = {'created_': 'created'})
comments_daily = comments_daily[comments_daily['created'] >= datetime(2022, 7, 23)]
plt.scatter(x = comments_daily['author_Organic'], y = comments_daily['author_AI'])
plt.xlabel('Unique commenters to r/Art')
plt.ylabel('Unique commenters to AI art subreddits')
plt.savefig(figures / 'unique_commenters_scatter.png')
plt.clf()

plt.scatter(x = comments_daily['id_Organic'], y = comments_daily['id_AI'])
plt.xlabel('Comments on r/Art')
plt.ylabel('Comments on AI art subreddits')
plt.savefig(figures / 'comments_scatter.png')
plt.clf()

comments_daily['comments_per_author_Organic'] = comments_daily['id_Organic'] / comments_daily['author_Organic']
comments_daily['comments_per_author_AI'] = comments_daily['id_AI'] / comments_daily['author_AI']
plt.scatter(x = comments_daily['comments_per_author_Organic'], y = comments_daily['comments_per_author_AI'])
plt.xlabel('Comments per author to r/Art')
plt.ylabel('Comments per author to AI art subreddits')
plt.savefig(figures / 'comments_per_author_scatter.png')
