from set_globals import *

from pathlib import Path
import pandas as pd
import numpy as np
import json
from datetime import datetime

from single_file import read_lines_zst

ai_subreddits = ['aiArt', 'StableDiffusion', 'midjourney', 'dalle2']
organic_subreddits = ['Art']
subreddits = ai_subreddits + organic_subreddits

# ----- Posts -----
posts_list = []
# Specific subreddit files (2022 and earlier)
for sub_file in raw.glob('*_submissions.zst'):
    for line, file_bytes_processed in read_lines_zst(raw / sub_file):
        obj = json.loads(line)
        created = datetime.fromtimestamp(int(obj['created_utc']))
        sub = {'subreddit': obj['subreddit'],
                'author': obj['author'],
                'created': created,
                'title': obj['title'],
                'score': obj['score'],
                'link_flair': obj['link_flair_text'],
               'id': obj['id']}
        posts_list.append(sub)

# 2023 submissions (preprocessed to include only the subreddits I'm using)
for sub_file in raw.glob('RS_2023-*'):
    for line, file_bytes_processed in read_lines_zst(raw / sub_file):
        obj = json.loads(line)
        created = datetime.fromtimestamp(int(obj['created_utc']))
        sub = {'subreddit': obj['subreddit'],
                'author': obj['author'],
                'created': created,
                'title': obj['title'],
                'score': obj['score'],
                'link_flair': obj['link_flair_text'],
               'id': obj['id']}
        posts_list.append(sub)

posts = pd.DataFrame(posts_list)

posts['year'] = posts['created'].dt.year
posts['month'] = posts['created'].dt.month
posts['day'] = posts['created'].dt.day

posts['link_flair'] = posts['link_flair'].apply(lambda x: x.replace(':a2:', '').strip() if isinstance(x, str) else x)

posts['ai_subreddit'] = posts['subreddit'].apply(lambda x: x in ai_subreddits)

ai_authors = set(posts[posts['ai_subreddit'] == True]['author'])
ai_authors = ai_authors - set(['[deleted]'])
art_authors = set(posts[posts['ai_subreddit'] == False]['author'])
art_authors = art_authors - set(['[deleted]'])
authors_both = ai_authors & art_authors

posts['author_both'] = posts['author'].apply(lambda x: x in authors_both)

posts.to_pickle(data / 'posts.pkl')

print(f'Number of AI authors: {len(ai_authors)}')
print(f'Number of Art authors: {len(art_authors)}')
print(f'Number of authors in both: {len(authors_both)}')

# ----- Comments -----
comments_list = []
for comment_file in raw.glob('*_comments.zst'):
    for line, file_bytes_processed in read_lines_zst(raw / comment_file):
        obj = json.loads(line)
        submission_id = obj['link_id'].split('_')[1]
        created = datetime.fromtimestamp(int(obj['created_utc']))
        comment = {'subreddit': obj['subreddit'],
                    'author': obj['author'],
                    'created': created,
                    'score': obj['score'],
                    'id': obj['id'],
                   'submission_id': submission_id}
        comments_list.append(comment)

# 2023 comments
for comment_file in raw.glob('RC_2023-*'):
    for line, file_bytes_processed in read_lines_zst(raw / comment_file):
        obj = json.loads(line)
        submission_id = obj['link_id'].split('_')[1]
        created = datetime.fromtimestamp(int(obj['created_utc']))
        comment = {'subreddit': obj['subreddit'],
                    'author': obj['author'],
                    'created': created,
                    'score': obj['score'],
                    'id': obj['id'],
                   'submission_id': submission_id}
        comments_list.append(comment)

comments = pd.DataFrame(comments_list)

comments['ai_subreddit'] = comments['subreddit'].apply(lambda x: x in ai_subreddits)

ai_commenters = set(comments[comments['ai_subreddit'] == True]['author'])
ai_commenters = ai_commenters - set(['[deleted]'])
art_commenters = set(comments[comments['ai_subreddit'] == False]['author'])
art_commenters = art_commenters - set(['[deleted]'])
commenters_both = ai_commenters & art_commenters

# Whether the comment author has comments in both AI subreddits and r/Art
comments['commenter_both'] = comments['author'].apply(lambda x: x in commenters_both)

comments.to_pickle(data / 'comments.pkl')

print(f'Number of AI commenters: {len(ai_commenters)}')
print(f'Number of Art commenters: {len(art_commenters)}')
print(f'Number of commenters in both: {len(commenters_both)}')

