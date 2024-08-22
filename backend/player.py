import pygame
from pydantic import BaseModel
import random


class Song(BaseModel):
    filepath: str
    name: str
    interpret: str
    playing: bool = False


class Player():
    def __init__(self):
        self.last_song_pos = 0
        self.last_song_id = 0
        self.playlist = []
        self.sound = None
        self.stop_force = False
        self.paused = False
        pygame.mixer.init()

    def set_last_song_pos(self, pos):
        self.last_song_pos = pos

    def jumpto(self, id, resume, start):
        self.play_music(id, resume, start)

    def play_music(self, id, resume, start: int = -1):
        self.paused = False
        if resume:
            id = self.last_song_id
        pygame.mixer.music.load(self.playlist[id].filepath)
        self.sound = pygame.mixer.Sound(self.playlist[id].filepath)
        print("playing song " + str(id))
        if resume:
            pygame.mixer.music.play(start=self.last_song_pos)
        elif start != -1:
            pygame.mixer.music.play(start=0)
            self.last_song_pos = start
            pygame.mixer.music.set_pos(start)
        else:
            self.last_song_pos = 0
            pygame.mixer.music.play(start=0)
            self.last_song_pos = -1
        print(id)
        self.playlist[id].playing = True
        while pygame.mixer.music.get_busy() and [self.playlist[id].playing]:
            if self.stop_force:
                return
            pygame.time.Clock().tick(10)
        print("trying next song")
        self.play_next_song()

    def play_next_song(self):
        index = 0
        song = self.playlist[index]
        while song.playing is False:
            index += 1
            if index < len(self.playlist):
                song = self.playlist[index]
            else:
                return
        if len(self.playlist) > index + 1:
            self.playlist[index].playing = False
            self.play_music(index + 1, False)

    def get_song_length(self):
        id, _ = self.find_playing_song()
        if id is None:
            return -1
        return self.sound.get_length()

    def get_song_length_file(self, file_path):
        return int(pygame.mixer.Sound(file_path).get_length())

    def stop_music(self):
        self.set_last_song_pos(self.get_song_position())
        _, song = self.find_playing_song()
        if song:
            song.playing = False
            pygame.mixer.music.stop()

    def pause_music(self):
        id, song = self.find_playing_song()
        if song:
            self.last_song_pos = self.get_song_position()
            self.last_song_id = id
            song.playing = False
            self.paused = True
            pygame.mixer.music.stop()

    def find_playing_song(self):
        song = next((song for song in self.playlist if song.playing), None)
        if song:
            index = self.playlist.index(song)
            return (index, song)
        else:
            print("No song is currently playing")
            return (None, None)

    def get_song_position(self):
        if self.last_song_pos == -1:
            return int(pygame.mixer.music.get_pos()/1000)
        else:
            return self.last_song_pos + int(pygame.mixer.music.get_pos()/1000)

    def set_playlist(self, new_list):
        self.playlist = new_list

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def shuffle(self):
        random.shuffle(self.playlist)


p = Player()
