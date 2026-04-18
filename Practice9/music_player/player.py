import pygame
import os

class Player:
    def __init__(self):
        pygame.mixer.init()

        base = os.path.dirname(os.path.abspath(__file__))
        music_folder = os.path.join(base, "music")

        self.songs = []
        for file_name in os.listdir(music_folder):
            if file_name.endswith(".mp3"):
                self.songs.append(os.path.join(music_folder, file_name))

        self.track_index = 0
        self.playing = False

    def play(self):
        pygame.mixer.music.load(self.songs[self.track_index])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self):
        self.track_index += 1
        if self.track_index >= len(self.songs):
            self.track_index = 0
        self.play()

    def prev_track(self):
        self.track_index -= 1
        if self.track_index < 0:
            self.track_index = len(self.songs) - 1
        self.play()

    def get_pos(self):
        return pygame.mixer.music.get_pos() // 1000