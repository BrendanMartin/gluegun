import json
from pprint import pprint

import requests
from praw import Reddit
from dotenv import load_dotenv
import os
import shutil

from config import dotenv_path, submission_download_dir

from log import get_logger

logger = get_logger(__name__)

load_dotenv(dotenv_path)

reddit = Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                user_agent='glue-gun-bot',
                username=os.environ.get('REDDIT_USERNAME'),
                password=os.environ.get('REDDIT_PASSWORD'))

def get_video_data(post_id):
    subm = reddit.submission(id=post_id)
    return dict(
        id=post_id,
        url=subm.media['reddit_video']['fallback_url'],
        duration=subm.media['reddit_video']['duration'],
        height=subm.media['reddit_video']['height'],
        width=subm.media['reddit_video']['width']
    )

def download_video(submission_id, video_url):
    dir_path = os.path.join(submission_download_dir, submission_id)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

        video_fp = os.path.join(dir_path, 'video.mp4')

        with requests.get(video_url, stream=True) as r:
            with open(video_fp, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return video_fp
    else:
        logger.info(f'Submission "{submission_id}" already downloaded')


def get_new_submissions(subreddit):
    subs = reddit.subreddit(subreddit).hot(limit=None)
    to_return = []
    for sub in subs:
        if sub.over_18 or not sub.is_video:
            continue
        to_return.append(sub)
    return to_return

def main():
    # download_video_from_submission('9qcbr9')
    subs = get_new_submissions('diwhy')
    subs = list(subs)
    print(subs[0])


if __name__ == '__main__':
    main()

