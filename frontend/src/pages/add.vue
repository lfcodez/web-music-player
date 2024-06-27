<template>
    <v-container fluid style="height: 75vH; width: 100vH;">
        <div style="margin-bottom: 25vH;"></div>
        <v-row justify="center">
            <v-card>
                <v-card-text style="width: 80vW;">
                    <h1>Paste Link</h1>
                    <v-text-field v-model="url" label="URL"></v-text-field>
                    <v-btn color="" flat @click="upload()">ADD</v-btn>
                </v-card-text>
            </v-card>
        </v-row>
    </v-container>
</template>

<script>
import { post } from '@/axios';
export default {
    name: 'Add',
    data() {
        return {
            url: '',
        }
    },
    // Your component's logic goes here
    methods: {
        async upload() {
            this.url = "";
            await post(`/song?url=${this.url}`);
        }
    }
}
</script>

<style scoped>
/* Your component's styles go here */
</style>