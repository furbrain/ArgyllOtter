#!/usr/bin/env python3

from gpiozero import Button


class Encoder():
    def __init__(self, pins, on_changed, on_pressed):
        self.on_changed = on_changed
        self.on_pressed = on_pressed
        self.clock = Button(pins[0])
        self.data = Button(pins[1])
        self.switch = Button(pins[2])
        self.pos = 0
        self.clock.when_pressed = self.movement
        self.switch.when_pressed = self.pressed    

    def movement(self):
        if self.data.is_pressed:
            self.pos +=1
        else:
            self.pos -=1
        self.on_changed(self.pos)

    def pressed(self):
        self.on_pressed()
        

if __name__=="__main__":
    enc = Encoder((19,13,26), print, lambda: print("Button"))
    input("press Enter to finish")
