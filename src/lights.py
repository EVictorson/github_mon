#!/usr/bin/env python3
from gpiozero import LED
import time

class Lights:
    def __init__(self):
        self.red_led_gpios = [17, 18, 27, 22]
        self.green_led_gpios = [19, 26, 20, 21]
        self.red_led_group = []
        self.green_led_group = []
        for i in range(len(self.red_led_gpios)):
            self.red_led_group.append(LED(self.red_led_gpios[i]))
            self.green_led_group.append(LED(self.green_led_gpios[i]))

    def turn_leds_on(self, led_group):
        for led in led_group:
            led.on()

    def turn_leds_off(self, led_group):
        for led in led_group:
            led.off()

    def blink_pattern(self, led_group, num_blinks):
        for i in range(num_blinks):
            self.turn_leds_on(led_group)
            time.sleep(0.5)
            self.turn_leds_off(led_group)
            time.sleep(0.5)
        self.turn_leds_on(led_group)

    def incremental_pattern(self, led_group):
        for led in led_group:
            led.on()
            time.sleep(0.5)

    def test_leds(self):
        self.blink_pattern(self.red_led_group, 5)
        self.turn_leds_off(self.red_led_group)
        self.blink_pattern(self.green_led_group, 5)
        self.turn_leds_off(self.green_led_group)
        self.incremental_pattern(self.red_led_group)
        self.incremental_pattern(self.green_led_group)

if __name__=='__main__':
    l = Lights()
    l.test_leds()


