var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        showSubmit: false,
        redditSubmURL: '',
        redditSubmID: '',
        redditVideoURL: '',
        disableURLSubmitBtn: false,
        disableExtractFramesBnt: false,
        videoData: [],
        videoFrames: {},
        showVideoFramesModal: false,
        showModalLoading: false,
        activeFramesRedditID: '',
        framesSelected: [],
        fetchVideosLoading: false,
        playbackRate: 1.0,
        playbackRates: [1.0, 1.5, 2.0, 2.5, 3.0].reverse()
    },
    created: function () {
        this.fetchVideos()
    },
    methods: {
        fetchVideos() {
            self.fetchVideosLoading = true;
            $.post('/_get_videos', {
                offset: this.videoData.length
            }).done(resp => {
                if (resp.result == 'rate-limit') {
                    // dunno
                }
                self.fetchVideosLoading = false;
                resp.result.map(elem => {
                    this.videoData.push(elem)
                });
            })
        },
        getRedditVideo() {
            this.disableURLSubmitBtn = true;

            $.post('/_get_reddit_video', {
                url: self.redditSubmURL
            }).done(resp => {
                self.disableURLSubmitBtn = false;
                if (!resp) {

                }
                this.redditVideoURL = resp['url'];
                this.redditSubmID = resp['id'];
            }).fail(() => {
                return false
            });
        },
        extractFrames(submissionID, videoURL) {
            if (Object.keys(this.videoFrames).length > 0) {
                return true;
            }
            this.disableExtractFramesBnt = true;
            this.showModalLoading = true;

            $.post('/_extract_frames', {
                submissionID: submissionID,
                videoURL: videoURL
            }).done(resp => {
                this.disableExtractFramesBnt = false;
                this.showModalLoading = false;
                this.videoFrames = resp;
            }).fail(() => {
                return false
            });
        },
        selectFrame(name) {
            if (this.framesSelected.includes(name)) {
                this.framesSelected.splice(this.framesSelected.indexOf(name, 1))
            } else {
                this.framesSelected.push(name)
            }
        },
        clearFrameSelections() {
            this.framesSelected = [];
        },
        saveSelections() {
            $.post('/_save_frame_selections', {
                reddit_id: this.activeFramesRedditID,
                framesSelected: JSON.stringify(this.framesSelected)
            }).done(resp => {
                this.framesSelected = [];
                this.videoData = this.videoData.filter(el => {
                    return el.reddit_id != this.activeFramesRedditID
                });
                this.videoFrames = {};
                return true;
            }).fail(() => {
                return false;
            });

        },
        noObject(reddit_video_id) {
            $.post('_no_object', {
                reddit_id: reddit_video_id
            }).done(resp => {
                return true;
            }).fail(() => {
                return false;
            });

            this.videoData = this.videoData.filter(el => {
                return el.reddit_id != reddit_video_id
            })
        },
        timeForward(reddit_id, amount) {
            this.$refs[reddit_id][0].currentTime += amount
        },
        stepBackward(reddit_id, amount) {
            this.$refs[reddit_id][0].currentTime -= amount
        },
        setPlaybackRate(reddit_id, rate) {
            this.playbackRate = rate;
            console.log(this.$refs[reddit_id][0]);
            this.$refs[reddit_id][0].playbackRate = rate
        }
    }
});