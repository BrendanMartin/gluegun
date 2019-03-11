"""
Implements functions for storing video frames both locally in a file system
and in a Google Cloud Storage bucket.

Schema:
extractor/submissions/  -> contains folders for each submission downloaded
extractor/submissions/2jr2j3/  -> folder for submission '2jr2j3' that holds video.mp4 and frames/ subfolder
extractor/submissions/2jr2j3/video.mp4  -> downloaded video from submission '2jr2j3'
extractor/submissions/2jr2j3/frames/  -> folder that holds .jpg frames of video from submission
extractor/submissions/2jr2j3/frames/01.jpg  -> frame 01 of 2jr2j3's video
"""
from tempfile import NamedTemporaryFile

import cv2
import os
import config
from flask import current_app
from google.cloud import storage

submissions_prefix = 'extractor/submissions/'
submission_frames_folder = submissions_prefix + '{submission_id}/frames/'

def _get_client():
    return storage.Client(os.getenv('GOOGLE_PROJECT_ID'))


def _get_bucket(client):
    return client.bucket(os.getenv('CLOUD_STORAGE_BUCKET'))


def store_image():
    client = _get_client()
    bucket = _get_bucket(client)


def store_frame(cv_image, submission_id, filename):
    with NamedTemporaryFile() as temp_file:
        temp_name = temp_file.name + '.jpg'
        cv2.imwrite(temp_name, cv_image)

        client = _get_client()
        bucket = _get_bucket(client)

        blob = bucket.blob(submission_frames_folder.format(submission_id=submission_id) + filename)
        blob.upload_from_filename(temp_name, content_type='image/jpeg')

        return blob.public_url



def check_exists(filename):
    client = _get_client()
    bucket = _get_bucket(client)
    stats = storage.Blob(bucket=bucket, name=filename).exists(client)
    return stats


def get_submission_path():
    client = _get_client()
    bucket = _get_bucket(client)


def video_is_downloaded(submission_id):
    client = _get_client()
    bucket = _get_bucket(client)
    name = submissions_prefix + submission_id + '/video.mp4'
    return storage.Blob(bucket=bucket, name=name).exists(client)


def frames_exist(submission_id):
    client = _get_client()
    bucket = _get_bucket(client)
    prefix = submissions_prefix + submission_id + '/frames/'
    return len(list(bucket.list_blobs(prefix=prefix, max_results=1))) > 0


def list_subfolders(prefix: str):
    """Lists subfolders under prefix. Requires trailing slash on prefix.
    E.g. prefix='/extractor/submissions/' will list all submissions in the submissions folder
    """
    client = _get_client()
    bucket = _get_bucket(client)
    iterator = bucket.list_blobs(delimiter='/', prefix=prefix)
    prefixes = set()
    for page in iterator.pages:
        prefixes.update(page.prefixes)
    return prefixes


if __name__ == '__main__':
    # print(check_exists('extractor/submissions/ay4hg6/'))
    # client = _get_client()
    # bucket = _get_bucket(client)
    # print(video_is_downloaded('ay4hg6'))
    # print(list(bucket.list_blobs(delimiter='/', prefix='extractor/submissions/')))
    # li = bucket.list_blobs(delimiter='/', prefix='extractor/submissions/')._get_next_page_response()
    # print(li['prefixes'])
    image = cv2.imread(r'C:\Users\Brendan\Projects\Misc\objdetect\objdetect\extractor\submissions\ay4hg6\frames\frame_00.jpg')
    store_frame(image, 'test', '00.jpg')
