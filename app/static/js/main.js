var urlSubmitBtn = document.getElementById('redditURLSubmit');

function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

function extractFrames() {

}

// urlSubmitBtn.addEventListener('click', function(e) {
//     var url_value = document.getElementById('redditURL').value;
//     var result = document.getElementById('result');
//
//     urlSubmitBtn.classList.add('disabled');
//     urlSubmitBtn.classList.add('loading');
//
//     $.post('/_get_reddit_video', {
//         url: url_value
//     }).done(function(resp) {
//         urlSubmitBtn.classList.remove('loading');
//         urlSubmitBtn.classList.remove('disabled');
//
//         var videoElem = document.getElementById('redditVideo');
//         document.removeChild(videoElem);
//
//         var videoElem = document.createElement('video');
//         setAttributes(videoElem, {
//             'id': 'redditVideo',
//             'width': '300px',
//             'controls': '',
//             'autoplay': '',
//             'name': 'media'
//         });
//
//         var sourceElem = document.createElement('source');
//         setAttributes(sourceElem, {
//            'type': 'video/mp4',
//             'src': resp['data']['url']
//         });
//
//         videoElem.appendChild(sourceElem);
//         result.appendChild(videoElem);
//
//         var extractFramesBtn = document.createElement('button');
//         setAttributes(extractFramesBtn, {
//            'class': 'btn btn-primary',
//            'id': 'extractFramesBtn'
//         });
//
//         result.appendChild(extractFramesBtn);
//         extractFramesBtn.addEventListener('click', extractFrames);
//
//         console.log(resp);
//     }).fail(function() {
//         return false
//     });
// });

var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        message: 'HELLO',
        redditSubmURL: '',
        redditSubmID: '',
        redditVideoURL: '',
        disableURLSubmitBtn: false,
        disableExtractFramesBnt: false,
        video_frames: {},
    },
    methods: {
        getRedditVideo() {
            var self = this;
            this.disableURLSubmitBtn = true;

            $.post('/_get_reddit_video', {
                url: self.redditSubmURL
            }).done(function (resp) {
                self.disableURLSubmitBtn = false;
                if (!resp) {
                    
                }
                self.redditVideoURL = resp['url'];
                self.redditSubmID = resp['id'];
                console.log(resp);
            }).fail(function () {
                return false
            });
        },
        extractFrames() {
            self = this;
            if (Object.keys(self.video_frames).length > 0) {
                return true;
            }
            this.disableExtractFramesBnt = true;

            $.post('/_extract_frames', {
               subm_id: self.redditSubmID
            }).done(function(resp) {
                self.disableExtractFramesBnt = false;
                self.video_frames = resp;
                console.log(resp)
            }).fail(function() {
                return false
            });

        },
    }
});