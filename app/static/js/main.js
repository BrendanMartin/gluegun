import Hello from './Hello.vue'
import Localizer from './Localizer.vue'
import VideoFramesModal from './VideoFramesModal.vue'

Vue.config.delimiters = ['${', '}'];

var app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        showSubmit: false,
        redditSubmURL: '',
        redditSubmID: '',
        redditVideoURL: '',
        videoData: [],
        showVideoFramesModal: false,
        activeFramesRedditID: '',
        fetchVideosLoading: false,
        playbackRate: 1.0,
        playbackRates: [1.0, 1.5, 2.0, 2.5, 3.0].reverse(),
        confirmNoObject: '',
        localizingImage: {
            url: '/submissions/agg8n5/frames/01.jpg',
            width: 608,
            height: 1080
        },
    },
    created: function () {
        this.fetchVideos();
    },
    components: {
        Hello,
        Localizer,
        VideoFramesModal
    },
    computed: {},
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
            this.$emit('extract-frames', submissionID, videoURL)
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
        timeForward(idx, amount) {
            this.$refs["video"][idx].currentTime += amount
        },
        stepBackward(idx, amount) {
            this.$refs["video"][idx].currentTime -= amount
        },
        setPlaybackRate(rate) {
            this.playbackRate = rate;
            console.log(this.$refs[reddit_id][0]);
            for (i = 0; i < this.$refs["video"].length; i++) {
                this.$refs["video"][i].playbackRate = rate
            }
        },
    }
});