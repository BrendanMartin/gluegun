<template>
    <div class="modal" id="videoFramesModal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Select Frames</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"
                            @click="clearFrameSelections()">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div v-show="framesLoading" class="frames-progress-wrapper">
                        <div class="progress">
                            <div class="progress-bar"
                                 role="progressbar"
                                 :aria-valuenow="framesProgress"
                                 aria-valuemin="0"
                                 aria-valuemax="100"
                                 :style="[ 'height: 20px', { width: framesProgress + '%' }]">
                                {{ framesProgress }}%
                            </div>
                        </div>
                        <div class="progress-text">
                            {{ framesProgressText }}
                        </div>
                    </div>
                    <template v-if="videoFrames.length > 0">
                        <div class="frames-container" v-show="!framesLoading">
                            <div v-for="(url, idx) in videoFrames" :key="idx"
                                 :class="['frame-outer', {selected:framesSelected.includes(idx + 1)}]">
                                <img :class="['frame', {selected:framesSelected.includes(idx + 1)}]"
                                     @click="selectFrame(idx + 1)" :src="url" @load="frameLoaded"/>
                                <i v-if="framesSelected.includes(idx + 1)" class="fas fa-check-circle"></i>

                            </div>
                        </div>
                    </template>
                </div>
                <div class="modal-footer">
                    <button type="button" @click="saveSelections()" data-dismiss="modal" class="btn btn-primary">
                        Save selections <span
                            v-if="framesSelected.length > 0"
                            class="badge badge-light">{{ framesSelected.length }}</span></button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal"
                            @click="clearFrameSelections()">Close
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                framesLoading: false,
                framesProgressText: '',
                videoFrames: [],
                framesSelected: [],
                activeFramesRedditID: '',
                framesProgress: 0,
                totalFramesLoaded: 0,
            }
        },
        methods: {
            extractFrames(submissionID, videoURL) {
                if (Object.keys(this.videoFrames).length > 0) {
                    return true;
                }
                this.activeFramesRedditID = submissionID;
                this.framesLoading = true;

                let source = new EventSource("/_extract_frames_v2"
                    + "?submissionID=" + submissionID
                    + "&videoURL=" + videoURL);

                source.addEventListener('progress', event => {
                    this.framesProgressText = 'Extracting frames...';
                    let data = JSON.parse(event.data);
                    this.framesProgress = Math.floor(parseFloat(data.progress) * 100);
                });

                source.addEventListener('paths', event => {
                    this.framesProgressText = 'Getting images...';
                    let data = JSON.parse(event.data);
                    this.videoFrames = data.paths;
                });

                source.addEventListener('done', event => {
                    console.log('done');
                    source.close();
                    this.$forceUpdate();
                });
            },
            frameLoaded() {
                let progress = this.totalFramesLoaded / this.videoFrames.length;
                this.framesProgress = Math.floor(progress * 100);
                this.framesProgressText = 'Loading images...';
                this.totalFramesLoaded += 1;
                if (this.totalFramesLoaded >= Object.keys(this.videoFrames).length) {
                    this.framesLoading = false;
                }
            },
            selectFrame(frame_num) {
                if (this.framesSelected.includes(frame_num)) {
                    this.framesSelected.splice(this.framesSelected.indexOf(frame_num, 1))
                } else {
                    this.framesSelected.push(frame_num)
                }
            },
            clearFrameSelections() {
                this.framesSelected = [];
            },
            saveSelections() {
                $.post('/_save_frame_selections', {
                    reddit_id: this.$parent.activeFramesRedditID,
                    framesSelected: JSON.stringify(this.framesSelected)
                }).done(resp => {
                    this.framesSelected = [];
                    this.videoData = this.videoData.filter(el => {
                        return el.reddit_id != this.$parent.activeFramesRedditID
                    });
                    this.videoFrames = {};
                    return true;
                }).fail(() => {
                    return false;
                });

            },
        }
    }
</script>

<style scoped>

</style>