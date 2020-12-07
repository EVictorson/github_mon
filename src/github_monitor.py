#!/usr/bin/env python3

""" depends on pygithub v1.54 and playsound and gpiozero"""
""" on rpi 3 w/ python 3 need to install:
    sudo apt install python3-gst-1.0
    pip3 install pygithub
    pip3 intall playsound
"""

import github as gh
from github import Github
import inspect
from playsound import playsound
import time
from datetime import datetime
from gpiozero import LED
import os
import pygame
import wave

class GithubMonitor:
    def __init__(self):
        self.token = os.getenv('POLLING_TOKEN')
        self.github = Github(self.token)
        self.repo_full = "TerraClear/tc_picker_control"
        self.repo = "tc_picker_control"
        self.branch_to_watch = 'dev'
        self.soundfile_dir = 'sounds/'
        self.last_run_number = 0
        self.last_conclusion = ''
        self.red_led_gpios = [17, 18, 27, 22]
        self.green_led_gpios = [19,26, 20, 21]
        self.led_enable = True
        self.red_led_group = []
        self.green_led_group = []
        if self.led_enable:
            for i in range(len(self.red_led_gpios)):
                self.red_led_group.append(LED(self.red_led_gpios[i]))
                self.green_led_group.append(LED(self.green_led_gpios[i]))

        self.success_soundfile = '/home/pi/vcs/rpi_ci/sounds/success/sm64_mario_yahoo.wav'
        self.failure_soundfile = '/home/pi/vcs/rpi_ci/sounds/failure/sm64_mario_falling.wav'
        self.pygame = pygame
        self.init_audio()

    def init_audio(self):
        file_wav_success = wave.open(self.success_soundfile)
        file_wav_failure = wave.open(self.failure_soundfile)
        self.freq_succ = file_wav_success.getframerate()
        self.freq_fail = file_wav_failure.getframerate()
        self.pygame.mixer.init(frequency=self.freq_succ)
        #self.failure_sound.mixer.init(frequency=freq_fail)
        #self.success_sound = pygame.mixer.init(frequency=freq_succ)
        #self.failure_sound = pygame.mixer.init(frequency=freq_fail)
        #self.success_sound.mixer.music.load(self.success_soundfile)
        #self.failure_sound.mixer.music.load(self.failure_soundfile)
    def play_failure(self):
        self.pygame.mixer.music.load(self.failure_soundfile)
        self.pygame.mixer.music.play()

    def play_success(self):
        self.pygame.mixer.music.load(self.success_soundfile)
        self.pygame.mixer.music.play()

    def run_loop(self):
        while(True):
            self.poll_github()
            time.sleep(60)

    def run(self):
        self.poll_github()

    def poll_github(self):
        print(datetime.now())
        repo = self.github.get_repo(self.repo_full)
        if repo.name == self.repo:
            workflows = repo.get_workflow_runs()[0]
            w = workflows
            print(w.id)
            print(w.head_branch)
            print(w.run_number)
            print(w.event)
            print(w.status)
            print(w.conclusion)
            print(w.workflow_id)
            print(w.created_at)
            print(w.updated_at)
            print(w.jobs_url)
            print(w.logs_url)
            print(w.check_suite_url)
            print(w.workflow_url)

            if self.last_run_number != w.run_number:
                if w.status == 'completed' and w.head_branch == self.branch_to_watch:
                    self.conclusion_check(w)
                    self.last_run_number = w.run_number
                    self.last_conclusion = w.conclusion

    def conclusion_check(self, workflow):
        if workflow.conclusion == 'failure':
            #playsound(self.failure_soundfile)
            #self.failure_sound.mixer.music.play()
            self.play_failure()
            if self.led_enable:
                self.blink_pattern(self.red_led_group)
        if workflow.conclusion == 'success':
            #playsound(self.success_soundfile)
            #self.success_sound.mixer.music.play()
            self.play_success()
            if self.led_enable:
                self.blink_pattern(self.green_led_group)

    def turn_leds_on(self, led_group):
        for led in led_group:
            led.on()

    def turn_leds_off(self, led_group):
        for led in led_group:
            led.off()

    def blink_pattern(self, led_group):
        for i in range(5):
            #led.on()
            self.turn_leds_on(led_group)
            time.sleep(0.5)
            #led.off()
            self.turn_leds_off(led_group)
            time.sleep(0.5)
        self.turn_leds_on(led_group)

if __name__=='__main__':
    gm = GithubMonitor()
    gm.run_loop()
