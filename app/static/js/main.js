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