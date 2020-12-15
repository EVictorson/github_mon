#!/usr/bin/env python3
import colorsys
import math
import unicornhathd
import time
from random import randint
import threading

class UnicornLights:
    blue = [0, 0, 255]
    green = [0, 255, 0]
    red = [255, 0, 0]
    wrd_rgb_passing = [
        [154, 173, 154], [0, 255, 0], [0, 235, 0], [0, 220, 0],
        [0, 185, 0], [0, 165, 0], [0, 128, 0], [0, 0, 0],
        [154, 173, 154], [0, 145, 0], [0, 125, 0], [0, 100, 0],
        [0, 80, 0], [0, 60, 0], [0, 40, 0], [0, 0, 0]]
    wrd_rgb_failing = [
        [154, 173, 154], [255, 0, 0], [235, 0, 0], [220, 0, 0],
        [185, 0, 0], [165, 0, 0], [128, 0, 0], [0, 0, 0],
        [154, 173, 154], [145, 0, 0], [125, 0, 0], [100, 0, 0],
        [80, 0, 0], [60, 0, 0], [40, 0, 0], [0, 0, 0]]

    def __init__(self, enable, brightness=1):
        unicornhathd.brightness(brightness)
        self.curr_wrd_rgb = self.wrd_rgb_passing
        self.status = 'passing'
        self.event = threading.Event()

    def __del__(self):
        unicornhathd.clear()

    def update_status(self, status):
        self.status = status
        if status == 'failing':
            self.curr_wrd_rgb = self.wrd_rgb_failing
        else:
            self.curr_wrd_rgb = self.wrd_rgb_passing

    def blink_red(self, num_blinks):
        self.blink(self.red, 5)

    def blink(self, rgb_list, num_blinks):
        for i in range(num_blinks):
            self.blink_all(rgb_list)

    def blink_all(self, rgb):
        unicornhathd.set_all(rgb[0], rgb[1], rgb[2])
        unicornhathd.show()
        time.sleep(0.5)
        unicornhathd.off()
        time.sleep(0.5)

    def play_matrix_animation(self, event_obj, is_passing, len_decisec=None):
        self.event_obj = event_obj
        wrd_rgb = self.wrd_rgb_passing
        if is_passing==True:
            wrd_rgb = self.wrd_rgb_passing
        else:
            wrd_rgb = self.wrd_rgb_failing
        self.matrix_animation_core(wrd_rgb, len_decisec)

    def matrix_animation_core(self, wrd_rgb, len_decisec=None):
        unicornhathd.rotation(90)
        unicornhathd.brightness(0.6)
        clock = 0
        stop = False
        if len_decisec is not None:
            clock_upper_lim = len_decisec

        blue_pilled_population = [[randint(0, 15), 15]]

        try:
            while not stop and not self.event_obj.is_set():
                for person in blue_pilled_population:
                    y = person[1]
                    for rgb in wrd_rgb:
                        if (y <= 15) and (y >= 0):
                            unicornhathd.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
                        y += 1
                    person[1] -= 1
                unicornhathd.show()
                time.sleep(0.1)
                clock += 1

                if clock % 5 == 0:
                    blue_pilled_population.append([randint(0, 15), 15])
                if clock % 7 == 0:
                    blue_pilled_population.append([randint(0, 15), 15])

                while len(blue_pilled_population) > 100:
                    blue_pilled_population.pop(0)

                if len_decisec is not None:
                    if clock == clock_upper_lim:
                        stop = True
                        unicornhathd.off()

        except KeyboardInterrupt:
            unicornhathd.off()
        unicornhathd.off()



if __name__=='__main__':
    ul = UnicornLights(True, 0.5)
    #ul.blink_red(5)
    #red = [255, 0, 0 ]
    #green = [0, 255, 0]
    #blue = [0, 0, 255]
    #blah = [125, 0, 125]
    #ul.blink(red, 5)
    #ul.blink(green, 5)
    #ul.blink(blue, 5)
    #ul.blink(blah, 5)
    ul.play_matrix_animation(True,100)
    #ul.update_status('failing')
    ul.play_matrix_animation(False,100)
    unicornhathd.off()

