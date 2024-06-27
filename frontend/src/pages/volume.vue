<template>
    <Navigation />
    <v-container>
        <h1>Volume</h1>
        <v-slider v-model="volume" step="1" max="100" @end="setVolume()"></v-slider>

    </v-container>
</template>

<script>
import { get, post } from '@/axios';

export default {
    name: 'Volume',
    data() {
        return {
            volume: 0,
        };
    },
    methods: {
        async setVolume() {
            await post(`/volume?volume=${this.volume/100}`)
        }
        , async getVolume() {
            let vol = await get(`/volume`)
            this.volume = Number.parseInt(vol*100)
        }

    },
    mounted() {
        this.getVolume();
    }
    // Your component's logic goes here
}
</script>

<style scoped>
/* Your component's styles go here */
</style>