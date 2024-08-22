<template>
    <v-container fluid class="ma-0 mt-n4">
        <v-container fluid class="fill-height pa-0 ma-0">
            <v-col class="pa-0 ma-0">

                <v-row justify="center" align="start" class="pa-0 ma-0">
                    <v-list class="pa-0 ma-0" style="overflow: hidden;">
                        <draggable :delay=75 :list="playlist" @change="move" class="pa-0 ma-0"
                            @start="(event) => event.item.classList.add('dragging')"
                            @end="(event) => event.item.classList.remove('dragging')">
                            <Song v-for="(song, index) in playlist" :song="song" class="my-1 pa-0"
                                @click.touch="play(index)" :isplaying="playlist[index].playing">
                            </Song>
                        </draggable>
                    </v-list>
                </v-row>

            </v-col>
        </v-container>
    </v-container>

    <div style="margin: 180px 0 0 0;"></div>

    <v-bottom-navigation class="px-8 pt-2" style="height: 180px;">




        <v-col class="pa-5">
            <v-row>
                <Song :song="playingSong || { 'name': '', 'interpret': '' }"></Song>
            </v-row>

            <v-row>
                <v-slider v-model="songPos" :max="songLength" step="1" @end="jumpTo"></v-slider>
            </v-row>
            <v-row justify="center" align="center" class="ma-0">
                <v-col align="center" style="text-align: center" class="py-0">
                    {{ Math.floor(songPos / 60) }}:{{ String(songPos % 60).padStart(2, '0') }}
                </v-col>
                <v-col align="center" class="py-0">
                    <v-btn v-if="paused" density="compact" flat icon="mdi-play" @click="play(-1, true)"></v-btn>
                    <v-btn v-if="!paused" density="compact" flat icon="mdi-pause" @click="pause()"></v-btn>
                </v-col>
                <v-col style="text-align: center" class="py-0">
                    {{ Math.floor(songLength / 60) }}:{{ String(songLength % 60).padStart(2, '0') }}
                </v-col>
            </v-row>
        </v-col>


    </v-bottom-navigation>

</template>

<script>
import { get, post, API_HOSTNAME, API_PORT } from '@/axios';
import { VueDraggableNext } from 'vue-draggable-next';
export default {
    name: 'Playlist',
    components: {
        draggable: VueDraggableNext,
    },
    data() {
        return {
            playlist: [],
            playingSong: null,
            songPos: 0,
            songLength: 0,
            lastSongPos: 0,
            switchedTime: false,
            paused: false,
        };
    },
    methods: {
        async getPlaylist() {
            this.playlist = await get("/playlist")
            this.playingSong = this.playlist.find(item => item?.playing == true)
        },
        async move() {
            await post("/playlist", this.playlist)
        },
        async play(id = -1, resume = false) {
            if (id == -1 && resume == true) id = 0;
            await get(`/play?id=${id}&resume=${resume}`)
            await this.getPlaylist()
            this.playingSong = this.playlist.find(item => item.id == id)
        },
        async pause() {
            await get(`/pause`);
        },
        async setSongPos() {
            this.songPos = await get("/position");
        },
        createSongPositionSocket() {
            let socket = new WebSocket(`ws://${API_HOSTNAME}:${API_PORT}/position`);
            socket.onopen = () => {
                socket.send("Hello from client");
            };
            socket.onmessage = (event) => {
                let data = JSON.parse(event.data);
                this.songPos = data.position;
                if (data.length != -1) this.songLength = Number.parseInt(data.length);
                this.paused = data.paused;
            }
        },
        createPlaylistSocket() {
            let socket = new WebSocket(`ws://${API_HOSTNAME}:${API_PORT}/playlist`);
            socket.onopen = () => {
                socket.send("Hello from client");
            };
            socket.onmessage = (event) => {
                let data = JSON.parse(event.data);
                this.playlist = data.playlist;
                this.playingSong = this.playlist.find(item => item.playing == true)
            }
        }
        , async jumpTo(val) {
            await post("/jumpto", { "id": this.playingSong.id, "time": val })
            await this.getPlaylist()
            this.playingSong = this.playlist.find(item => item.playing == true)
        }
    },
    mounted() {
        // this.switchedTime = true;
        this.getPlaylist()
        this.createPlaylistSocket()
        this.createSongPositionSocket()
    },
    watch: {

    }
};
</script>

<style>
.dragging {
    background-color: rgba(248, 248, 255, 0.133);
    
}
</style>