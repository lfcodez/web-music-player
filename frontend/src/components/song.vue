<template>

    <v-container style="width: 70vW;" class="py-1 px-5 mx-0">
        <v-container v-if="isplaying" style="padding: 0px;" class="highlighted-container">

            <p class="text-h7">
                {{ song.name }} <v-icon style="position: absolute; right: 15px; opacity: 40%;">mdi-music</v-icon>
            </p>
            <p class="text-caption">
                {{ song.interpret }}
            </p>

        </v-container>
        <v-container v-if="!isplaying" style="padding: 0px;">
            <p class="text-h7">
                {{ song.name }}
            </p>
            <p class="text-caption">
                {{ song.interpret }}
            </p>
        </v-container>

    </v-container>

</template>

<script>
export default {
    name: 'Song',
    props: {
        song: {
            type: Object,
            required: true
        },
        isplaying: {
            type: Boolean,
            required: false
        }
    },
    data() {
        return {
        };
    },
    mounted() {

    }
    // Your component logic goes here
}
</script>

<style scoped>
.highlighted-container {
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 1px 0px inset, rgba(200, 200, 93, 0.25) 0px 50px 100px -20px, rgba(255, 255, 255, 0.3) 0px 30px 60px -30px;
}
</style>