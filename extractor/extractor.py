import os
from time import sleep

import cv2
import config
if os.getenv('USE_CLOUD_STORAGE') == '1':
    from gstorage import store_frame
else:
    from .storage import store_frame

from log import get_logger
logger = get_logger(__name__)


def zero_pad_frame(frame, total_frames):
    fr = str(frame)
    tfr = str(total_frames)
    while len(fr) < len(tfr):
        fr = '0' + fr
    return fr


def extract_frames(submission_id, video_url):
    video = cv2.VideoCapture(video_url)

    fps = video.get(cv2.CAP_PROP_FPS)
    frameCount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frameCount / fps)
    stored_image_paths = []

    count = 0
    second = 1
    success = 1
    while success:
        success, image = video.read()
        if count % fps == 0:    # capture one frame per second
            frame_num = zero_pad_frame(second, duration)
            filename = f'{frame_num}.jpg'
            stored_path = store_frame(image, submission_id, filename)
            yield dict(path=stored_path, progress=second / duration)
            # stored_image_paths.append(store_frame(image, submission_id, filename))
            second += 1

        count += 1

    video.release()
    cv2.destroyAllWindows()
    # return stored_image_paths

def main():
    print(zero_pad_frame(1, 3546))

    # extract_frames()

if __name__ == '__main__':
    main()