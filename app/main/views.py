from time import sleep

import os
from flask import render_template, request, jsonify, send_from_directory

from app.main import main
from app.main.forms import FindRedditVideoForm
from config import submission_download_dir
from extractor.extractor import video_is_downloaded, frames_extracted, extract_frames, get_paths_of_frames
from reddit_api import get_video_data, download_video_from_submission


@main.route('/')
def index():
    url_form = FindRedditVideoForm()
    return render_template('index.html', url_form=url_form)

@main.route('/_get_reddit_video', methods=['POST'])
def _get_reddit_video():
    url = request.form.get('url')
    print(url)
    if not url:
        return jsonify({})
    url = [x for x in url.split('/') if x]
    subm_id = url[-2]

    data = get_video_data(subm_id)
    return jsonify(data)

@main.route('/_extract_frames', methods=['POST'])
def _extract_frames():
    subm_id = request.form.get('subm_id')

    if not video_is_downloaded(subm_id):
        download_video_from_submission(subm_id)

    extract_frames(subm_id)
    paths = get_paths_of_frames(subm_id)
    for name, path in paths.copy().items():
        new_path = path.split('extractor')[-1]
        new_path = new_path.replace('\\', '/')
        paths[name] = new_path
    return jsonify(paths)


@main.route('/_refresh_videos')
def refresh_videos():
    pass


@main.route('/submissions/<path:filename>')
def submission_frames(filename):
    return send_from_directory(submission_download_dir, filename, as_attachment=True)