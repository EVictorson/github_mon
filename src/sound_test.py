#!/usr/bin/env python3

#from playsound import playsound
import pygame
import wave

if __name__=="__main__":
    fpath = '/home/pi/vcs/rpi_ci/sounds/success/sm64_mario_yahoo.wav'
    file_wav = wave.open(fpath)
    freq = file_wav.getframerate()
    pygame.mixer.init(frequency=freq)
    pygame.mixer.music.load(fpath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

