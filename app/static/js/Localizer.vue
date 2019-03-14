<template>
    <div>
        <button @click="setLocalize()">Localize</button>
        <div id="canvas"
             ref="canvas"
             v-show="localize"
             @mousedown="mouseDown"
             @mousemove="mouseMoving"
             @mouseup="mouseUp"
            :style="canvasStyle">
            <div class="bbox"
                 ref="bbox"
                 :style="bboxStyle">
            </div>
        </div>
        <button @click="saveBbox">Save</button>

        <p>Mouse coords: ({{ mouse.x }}, {{ mouse.y }})</p>
        <p>Bounding box: ({{ bbox_x }}, {{ bbox_y }}),
            width: {{ bbox_width }}, height: {{ bbox_height }}</p>
    </div>

</template>

<script>
    export default {
        data() {
            return {
                localize: false,
                dragging: false,
                canvas: {
                    height: '',
                    width: '',
                },
                mouse: {
                    x: '',
                    y: ''
                },
                bbox_x: '',
                bbox_y: '',
                bbox_height: 0,
                bbox_width: 0
            }
        },
        computed: {
            bboxStyle() {
                return {
                    position: 'absolute',
                    top: this.bbox_y,
                    left: this.bbox_x,
                    height: this.bbox_height,
                    width: this.bbox_width
                };
            },
            canvasStyle() {
                return {
                    'backgroundImage': 'url(' + this.$parent.localizingImage.url + ')',
                    height: this.$parent.localizingImage.height,
                    width: this.$parent.localizingImage.width
                }
            }
        },
        methods: {
            setLocalize() {
                this.localize = !this.localize
            },
            mouseDown() {
                if (!this.dragging) {
                    console.log('Starting drag');
                    this.dragging = true;
                    this.bbox_width = 0;
                    this.bbox_height = 0;
                    this.bbox_x = this.mouse.x;
                    this.bbox_y = this.mouse.y;
                }
            },
            mouseMoving(e) {
                this.mouse.x = e.clientX - this.$refs['canvas'].getBoundingClientRect().left;
                this.mouse.y = e.clientY - this.$refs['canvas'].getBoundingClientRect().top;

                if (this.dragging) {
                    this.bbox_height = this.mouse.y - this.bbox_y;
                    this.bbox_width = this.mouse.x - this.bbox_x;
                }
            },
            mouseUp() {
                console.log('Stopped drag');
                if (this.dragging) {
                    this.dragging = false;
                }
            },
            saveBbox() {
                // Flip y-coord for regular x,y axis
                let flipped_y = this.canvas.height - this.bbox_y;
                let bbox = {
                    x: this.bbox_x,
                    y: flipped_y,
                    height: this.bbox_height,
                    width: this.bbox_width
                };

                $.post('/_save_bbox', {
                    image: this.$parent.localizingImage,
                    bbox: JSON.stringify(bbox)
                }).done(resp => {

                }).fail(resp => {

                });
            }
        },
        mounted() {
            document.addEventListener('mouseup', this.mouseUp())
        }
    }
</script>

<!--<style lang="scss" scoped>-->
<style scoped>
    #canvas {
        position: relative;
        width: 1000px;
        height: 1000px;
        border: 1px solid black;
    }

    button {

    }

    .bbox {
        border: 1px solid red;
    }


</style>