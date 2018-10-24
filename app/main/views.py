from time import sleep

from flask import render_template, request, jsonify

from app.main import main
from app.main.forms import FindRedditVideoForm
from extractor.extractor import video_is_downloaded, frames_extracted
from reddit_api import get_video_data


@main.route('/')
def index():
    url_form = FindRedditVideoForm()
    return render_template('index.html', url_form=url_form)

@main.route('/_get_reddit_video', methods=['POST'])
def _get_reddit_video():
    url = request.form.get('url')
    if not url:
        sleep(3)
        return jsonify({})
    url = [x for x in url.split('/') if x]
    subm_id = url[-2]

    if video_is_downloaded(subm_id):
        if frames_extracted(subm_id):
            pass
        else:
            pass
    else:
        pass

    data = get_video_data(subm_id)
    return jsonify(dict(data=data))