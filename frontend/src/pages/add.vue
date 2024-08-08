<template>
    <v-container fluid style="height: 75vH; width: 100vH;">
        <div style="margin-bottom: 25vH;"></div>
        <v-row justify="center">
            <v-card>
                <v-card-text style="width: 80vW;">
                    <h1>Link einfügen:</h1>
                    <v-text-field v-model="url" label="URL"></v-text-field>
                    <v-btn :loading="loading" color="" flat @click="upload()">ADD</v-btn>
                </v-card-text>
            </v-card>
        </v-row>
    </v-container>
    <v-snackbar v-model="snackbar" multi-line>
        Ein Fehler ist aufgetreten.
        <template v-slot:actions>
            <v-btn color="red" variant="text" @click="snackbar = false">
                Close
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
import { post } from '@/axios';
export default {
    name: 'Add',
    data() {
        return {
            url: '',
            loading: false,
            snackbar: false,
        }
    },
    // Your component's logic goes here
    methods: {
        async upload() {
            if (this.loading) return;
            this.loading = true;
            try {
                await post(`/song?url=${this.url}`);
            } catch (e) {
                console.error(e);
                this.snackbar = true;
            }
            this.loading = false;
            this.url = '';
        }
    }
}
</script>

<style scoped>
/* Your component's styles go here */
</style>