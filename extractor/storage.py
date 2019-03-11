import cv2
import os

from config import submission_download_dir

"""Video and frames storage for local file system"""


def video_is_downloaded(submission_id):
    path = os.path.join(submission_download_dir, submission_id, 'video.mp4')
    return os.path.exists(path)


def frames_extracted(submission_id):
    path = os.path.join(submission_download_dir, submission_id, 'frames')
    return os.path.exists(path)


def get_video_path(submission_id):
    return os.path.join(submission_download_dir, submission_id, 'video.mp4')


def get_paths_of_frames(submission_id):
    path = os.path.join(submission_download_dir, submission_id, 'frames')
    return {x.name.split('.')[0]: x.path for x in os.scandir(path)}


def get_submission_path(submission_id):
    return os.path.join(submission_download_dir, submission_id)


def check_frames_exist(submission_id):
    spath = get_submission_path(submission_id)
    return os.path.exists(os.path.join(spath, 'frames'))


def submissions_to_extract():
    submission_paths = [f.path for f in os.scandir(submission_download_dir)]
    to_return = []
    for spath in submission_paths:
        if not 'frames' in os.listdir(spath):
            to_return.append(spath)
    return to_return


def store_frame(cv_image, submission_id, filename):
    frame_path = os.path.join(get_submission_path(submission_id), 'frames')
    os.mkdir(frame_path)
    image_path = os.path.join(frame_path, filename)
    cv2.imwrite(cv_image, image_path)
    return image_path