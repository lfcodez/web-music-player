<template>
    <v-container class="my-0 py-0" style="padding-left: 25vW">
        <v-speed-dial location="right" transition="fade-transition" fluid>
            <template v-slot:activator="{ props: activatorProps }">
                <v-fab v-bind="activatorProps" size="large" icon="$vuetify" class="my-10"></v-fab>
            </template>
            <div class="mr-14"></div>
            <v-btn key="1" icon="mdi-playlist-play" router to="/"></v-btn>
            <v-btn key="2" icon="mdi-plus" router to="/add"></v-btn>
            <v-btn key="3" icon="mdi-volume-high" router to="/volume"></v-btn>
        </v-speed-dial>
    </v-container>
</template>

<script>
export default {
    name: 'Navigation',
    // Your component's logic goes here
}
</script>

<style scoped>
/* Your component's styles go here */
</style>