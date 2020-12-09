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
import sys
from sound import Sound
from lights import Lights

class GithubMonitor:
    def __init__(self):
        self.token = os.getenv('POLLING_TOKEN')
        self.github = Github(self.token)
        self.repo_full = "TerraClear/tc_picker_control"
        self.repo = "tc_picker_control"
        self.branch_to_watch = 'dev'
        self.sound = Sound(False)
        self.last_run_number = 0
        self.last_conclusion = ''
        self.led_enable = True
        self.lights = Lights(self.led_enable)
        self.sleep_time_sec = 20

    def run_loop(self):
        while(True):
            self.poll_github()
            time.sleep(self.sleep_time_sec)

    def run(self):
        self.poll_github()

    def poll_github(self):
        repo = self.github.get_repo(self.repo_full)
        if repo.name == self.repo:
            workflows = repo.get_workflow_runs()[0]
            w = workflows

            if self.last_run_number != w.run_number:
                print('\n')
                print('Report Time: {}'.format(datetime.now()))
                print('ID = {}'.format(w.id))
                print('Branch = {}'.format(w.head_branch))
                print('Workflow id = {}'.format(w.workflow_id))
                print('Workflow Created At {}'.format(w.created_at))
                print('Workflow Updated At {}'.format(w.updated_at))
                print('Workflow Run Number = {}'.format(w.run_number))
                print('Workflow Trigger Event = {}'.format(w.event))
                print('Workflow Status = {}'.format(w.status))
                print('Workflow Conclusion = {}'.format(w.conclusion))

                if w.status == 'completed' and w.head_branch == self.branch_to_watch:
                    self.conclusion_check(w)
                    self.last_run_number = w.run_number
                    self.last_conclusion = w.conclusion

    def conclusion_check(self, workflow):
        if workflow.conclusion == 'failure':
            self.sound.play_failure()
            if self.led_enable:
                self.lights.blink_pattern_red(5)
                self.lights.incremental_pattern_red()
        if workflow.conclusion == 'success':
            self.sound.play_success()
            if self.led_enable:
                self.lights.blink_pattern_green(5)
                self.lights.incremental_pattern_green()

if __name__=='__main__':
    gm = GithubMonitor()
    gm.run_loop()
