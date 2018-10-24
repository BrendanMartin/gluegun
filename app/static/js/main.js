var urlSubmitBtn = document.getElementById('redditURLSubmit');

function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}

function extractFrames() {

}

urlSubmitBtn.addEventListener('click', function(e) {
    var url_value = document.getElementById('redditURL').value;
    var result = document.getElementById('result');

    urlSubmitBtn.classList.add('disabled');
    urlSubmitBtn.classList.add('loading');

    $.post('/_get_reddit_video', {
        url: url_value
    }).done(function(resp) {
        urlSubmitBtn.classList.remove('loading');
        urlSubmitBtn.classList.remove('disabled');

        var videoElem = document.getElementById('redditVideo');
        document.removeChild(videoElem);

        var videoElem = document.createElement('video');
        setAttributes(videoElem, {
            'id': 'redditVideo',
            'width': '300px',
            'controls': '',
            'autoplay': '',
            'name': 'media'
        });

        var sourceElem = document.createElement('source');
        setAttributes(sourceElem, {
           'type': 'video/mp4',
            'src': resp['data']['url']
        });

        videoElem.appendChild(sourceElem);
        result.appendChild(videoElem);

        var extractFramesBtn = document.createElement('button');
        setAttributes(extractFramesBtn, {
           'class': 'btn btn-primary',
           'id': 'extractFramesBtn'
        });

        result.appendChild(extractFramesBtn);
        extractFramesBtn.addEventListener('click', extractFrames);

        console.log(resp);
    }).fail(function() {
        return false
    });
});

