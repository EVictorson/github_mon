#!/usr/bin/env python3

import pygame
import wave
from os import walk
import random
import time

class Sound:
    def __init__(self):
        self.success_files = []
        self.failure_files = []
        self.success_dir = '/home/pi/vcs/rpi_ci/sounds/success/'
        self.failure_dir = '/home/pi/vcs/rpi_ci/sounds/failure/'
        self.pygame = pygame
        self.load_files()
        self.clock = pygame.time.Clock()

    def load_files(self):
        self.load_files_in_dir(self.success_dir, self.success_files)
        self.load_files_in_dir(self.failure_dir, self.failure_files)

    def load_files_in_dir(self, dir, files_list):
        for (dirpath, dirnames, filenames) in walk(dir):
            files_list.extend(filenames)
            break

    def play_failure(self):
        #self.play_rand_file(self.failure_files)
        file = self.select_rand_file(self.failure_files)
        fpath = self.failure_dir + file
        freq = self.get_freq(fpath)
        self.pygame.mixer.init(frequency=freq)
        #self.pygame.mixer.music.load(file)
        #self.pygame.mixer.music.play()
        sound = self.pygame.mixer.Sound(fpath)
        sound.play()
        time.sleep(sound.get_length()+1)

    def play_success(self):
        file = self.select_rand_file(self.success_files)
        fpath = self.success_dir + file
        print("file chosen = {}".format(fpath))
        freq = self.get_freq(fpath)
        self.pygame.mixer.init(frequency=freq)
        sound = self.pygame.mixer.Sound(fpath)
        sound.play()
        time.sleep(sound.get_length()+1)

    def play_rand_file(self, audio_list):
        file = self.select_rand_file(audio_list)
        fpath = self.failure_dir + file
        freq = self.get_freq(fpath)
        self.pygame.mixer.init(frequency=freq)
        self.pygame.mixer.music.load(fpath)
        self.pygame.mixer.music.play()

    def select_rand_file(self, audio_list):
        x = random.randint(0, len(audio_list)-1)
        return audio_list[x]

    def get_freq(self, fpath):
        file = wave.open(fpath)
        freq = file.getframerate()
        return freq

if __name__=='__main__':
    s = Sound()
    for i in range(4):
        s.play_success()
        s.play_failure()
