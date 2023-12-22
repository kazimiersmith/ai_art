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

subs_list = []
# Specific subreddit files (2022 and earlier)
for sub_file in data.glob('*_submissions.zst'):
    for line, file_bytes_processed in read_lines_zst(data / sub_file):
        obj = json.loads(line)
        created = datetime.fromtimestamp(int(obj['created_utc']))
        if created.year >= 2022:
            sub = {'subreddit': obj['subreddit'],
                    'author': obj['author'],
                    'created': created,
                    'title': obj['title'],
                    'score': obj['score'],
                    'link_flair': obj['link_flair_text'],
                   'id': obj['id']}
            subs_list.append(sub)

# 2023 submissions (preprocessed to include only the subreddits I'm using)
for sub_file in data.glob('RS_2023-*'):
    for line, file_bytes_processed in read_lines_zst(data / sub_file):
        obj = json.loads(line)
        created = datetime.fromtimestamp(int(obj['created_utc']))
        if created.year >= 2022:
            sub = {'subreddit': obj['subreddit'],
                    'author': obj['author'],
                    'created': created,
                    'title': obj['title'],
                    'score': obj['score'],
                    'link_flair': obj['link_flair_text'],
                   'id': obj['id']}
            subs_list.append(sub)

subs = pd.DataFrame(subs_list)

subs['year'] = subs['created'].dt.year
subs['month'] = subs['created'].dt.month
subs['day'] = subs['created'].dt.day

subs['link_flair'] = subs['link_flair'].apply(lambda x: x.replace(':a2:', '').strip() if isinstance(x, str) else x)

subs['ai_subreddit'] = subs['subreddit'].apply(lambda x: x in ai_subreddits)

subs.to_pickle(data / 'subs.pkl')

ai_authors = set(subs[subs['ai_subreddit'] == True]['author'])
art_authors = set(subs[subs['ai_subreddit'] == False]['author'])

print(f'Number of AI authors: {len(ai_authors)}')
print(f'Number of Art authors: {len(art_authors)}')
print(f'Number of authors in both: {len(ai_authors & art_authors)}')

comments_list = []
for comment_file in data.glob('*_comments.zst'):
    for line, file_bytes_processed in read_lines_zst(data / comment_file):
        obj = json.loads(line)
        submission_id = obj['link_id'].split('_')[1]
        created = datetime.fromtimestamp(int(obj['created_utc']))
        if created.year >= 2022:
            comment = {'subreddit': obj['subreddit'],
                        'author': obj['author'],
                        'created': created,
                        'score': obj['score'],
                        'id': obj['id'],
                       'submission_id': submission_id}
            comments_list.append(comment)

# 2023 comments
for comment_file in data.glob('RC_2023-*'):
    for line, file_bytes_processed in read_lines_zst(data / comment_file):
        obj = json.loads(line)
        submission_id = obj['link_id'].split('_')[1]
        created = datetime.fromtimestamp(int(obj['created_utc']))
        if created.year >= 2022:
            comment = {'subreddit': obj['subreddit'],
                        'author': obj['author'],
                        'created': created,
                        'score': obj['score'],
                        'id': obj['id'],
                       'submission_id': submission_id}
            comments_list.append(comment)

comments = pd.DataFrame(comments_list)
comments['ai_subreddit'] = comments['subreddit'].apply(lambda x: x in ai_subreddits)
comments.to_pickle(data / 'comments.pkl')

ai_commenters = set(comments[comments['ai_subreddit'] == True]['author'])
art_commenters = set(comments[comments['ai_subreddit'] == False]['author'])
print(f'Number of AI commenters: {len(ai_commenters)}')
print(f'Number of Art commenters: {len(art_commenters)}')
print(f'Number of commenters in both: {len(ai_commenters & art_commenters)}')

