import json
import os
from math import floor

import cv2

from config import submission_download_dir
from log import get_logger

logger = get_logger(__name__)

def get_duration(submission_id):
    with open(os.path.join(submission_download_dir, submission_id, 'data.json')) as f:
        return json.load(f)['duration']

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

def submissions_to_extract():
    submission_paths = [f.path for f in os.scandir(submission_download_dir)]
    to_return = []
    for spath in submission_paths:
        if not 'frames' in os.listdir(spath):
            to_return.append(spath)
    return to_return

def get_submission_path(submission_id):
    return os.path.join(submission_download_dir, submission_id)

def zero_pad_frame(frame, total_frames):
    fr = str(frame)
    tfr = str(total_frames)
    while len(fr) < len(tfr):
        fr = '0' + fr
    return fr

def extract_frames(submission_id=None):
    if submission_id:
        subm_path = get_submission_path(submission_id)
        if os.path.exists(os.path.join(subm_path, 'frames')):
            return True
        submission_paths = [subm_path]
    else:
        submission_paths = submissions_to_extract()

    for spath in submission_paths:
        logger.info('Extracting frames')
        frame_path = os.path.join(spath, 'frames')
        os.mkdir(frame_path)

        video_path = os.path.join(spath, 'video.mp4')
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(frameCount / fps)

        # TODO zero pad frame names by calculating total number of frames first to find number of zeros to prepend
        count = 0
        second = 0
        success = 1
        while success:
            success, image = video.read()
            if count % fps == 0:    # capture one frame per second
                frame_num = zero_pad_frame(second, duration)
                image_path = os.path.join(frame_path, f'{frame_num}.jpg')
                cv2.imwrite(image_path, image)
                second += 1

            count += 1

        video.release()
    cv2.destroyAllWindows()

def main():
    print(zero_pad_frame(1, 3546))

    # extract_frames()

if __name__ == '__main__':
    main()