from datetime import datetime, timedelta
from time import sleep

import os
import json
from flask import render_template, request, jsonify, send_from_directory, session, current_app

from app.main import main
from app.main.forms import FindRedditVideoForm
from config import submission_download_dir
from db import retrieve_videos, store_frame_selections, store_object_not_in_video, update_submissions, \
    compute_statistics
from log import get_logger
from reddit_api import get_video_data, download_video, get_new_submissions
from extractor.extractor import extract_frames

logger = get_logger(__name__)

if current_app.config.get('FLASK_CONFIG') == 'prod':
    logger.info('Using Google Cloud Storage')
    from gstorage import video_is_downloaded, frames_exist
else:
    from extractor.storage import video_is_downloaded, frames_exist


@main.before_request
def init_session():
    data = dict(
            labeled=[],
            subreddit='diwhy',
            last_reddit_update=0
    )
    for k, v in data.items():
        if k not in session.keys():
            session[k] = v


@main.route('/')
def index():
    url_form = FindRedditVideoForm()
    videos = retrieve_videos()
    return render_template('index.html', url_form=url_form, videos=json.dumps(videos))


@main.route('/stats')
def stats():
    stats = compute_statistics()
    return render_template("stats.html", stats=stats)


@main.route('/localization')
def localization():
    return "<h1>Localization</h1>"



@main.route('/_get_videos', methods=['POST'])
def get_vidoes():
    offset = int(request.form.get('offset'))
    videos = retrieve_videos(offset, session['labeled'])

    if not videos:
        last_update = datetime.utcfromtimestamp(session['last_reddit_update'])
        if datetime.utcnow() - last_update > timedelta(seconds=60):
            update_submissions(session['subreddit'])
            videos = retrieve_videos(offset, session['labeled'])
        else:
            return jsonify({"result": "rate-limit"})

    return jsonify({"result": videos})


@main.route('/_get_reddit_video', methods=['POST'])
def _get_reddit_video():
    url = request.form.get('url')
    if not url:
        return jsonify({})
    url = [x for x in url.split('/') if x]
    subm_id = url[-2]

    data = get_video_data(subm_id)
    return jsonify(data)


@main.route('/_extract_frames', methods=['POST'])
def _extract_frames():
    submission_id = request.form.get('submissionID')
    video_url = request.form.get('videoURL')

    # Changed to stream to CV2 right from video URL
    # if not video_is_downloaded(submission_id):
    #     download_video(submission_id, video_url)

    # Check if frames already extracted

    if not frames_exist(submission_id):
        paths = extract_frames(submission_id, video_url)

    paths = get_paths_of_frames(submission_id)

    for name, path in paths.copy().items():
        new_path = path.split('extractor')[-1]
        new_path = new_path.replace('\\', '/')
        paths[name] = new_path

    return jsonify(paths)


@main.route('/_refresh_videos')
def refresh_videos():
    pass


@main.route('/_save_frame_selections', methods=['POST'])
def save_frame_selections():
    reddit_id = request.form.get('reddit_id')
    selections = json.loads(request.form.get('framesSelected'))
    selections = sorted([int(s.split('_')[-1]) for s in selections])
    store_frame_selections(reddit_id, selections)

    session['labeled'].append(reddit_id)
    session.modified = True

    return jsonify({"result": "success"})


@main.route('/_no_object', methods=['POST'])
def object_not_in_video():
    reddit_id = request.form.get('reddit_id')
    store_object_not_in_video(reddit_id)
    return jsonify({"result": "success"})


@main.route('/submissions/<path:filename>')
def submission_frames(filename):
    return send_from_directory(submission_download_dir, filename, as_attachment=True)