import json
import os
from math import floor

import cv2

from config import submission_download_dir


def get_duration(submission_id):
    with open(os.path.join(submission_download_dir, submission_id, 'data.json')) as f:
        return json.load(f)['duration']

def video_is_downloaded(submission_id):
    path = os.path.join(submission_download_dir, submission_id, 'video.mp4')
    return os.path.exists(path)

def frames_extracted(submission_id):
    path = os.path.join(submission_download_dir, submission_id, 'frames')
    return os.path.exists(path)

def submissions_to_extract():
    submission_paths = [f.path for f in os.scandir(submission_download_dir)]
    to_return = []
    for spath in submission_paths:
        if not 'frames' in os.listdir(spath):
            to_return.append(spath)
    return to_return

def extract_frames():
    submission_paths = submissions_to_extract()

    for spath in submission_paths:
        frame_path = os.path.join(spath, 'frames')
        os.mkdir(frame_path)

        video_path = os.path.join(spath, 'video.mp4')
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)

        count = 0
        second = 0
        success = 1
        while success:
            success, image = video.read()
            if count % fps == 0:    # capture one frame per second
                image_path = os.path.join(frame_path, f'frame_{second}.jpg')
                cv2.imwrite(image_path, image)
                second += 1

            count += 1

        video.release()
    cv2.destroyAllWindows()

def main():
    extract_frames()

if __name__ == '__main__':
    main()