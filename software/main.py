#!/usr/bin/env python3

import asyncio
import collections
#import menu
#import hardware
from functools import partial
from modes import messages
from approxeng.input.selectbinder import ControllerResource

class DiscardingQueue(collections.deque):
    def __init__(self, maxlen):
        super().__init__(maxlen=maxlen)
        
    def put(self,item):
        self.append(item)
    
    def get(self):
        return self.popleft()

class Main:
    def __init__(self):
        self.events = DiscardingQueue(20)
        self.mode = None
        self.mode_task = None
        self.finished = False
        #set up controller if present

    async def run(self):
        #set up encoder
        loop = asyncio.get_event_loop()
        #encoder = hardware.Encoder((19,13,26), self.handle_encoder_change, self.handle_encoder_press)
        loop.create_task(self.controller_monitor())
        loop.create_task(self.poll_events())
        while not self.finished:
            await asyncio.sleep(0.1)
       
    def enter_mode(self, mode):
        if self.mode_task:
            self.mode_task.cancel()
        self.mode = mode(self.joystick)
        self.mode_task = asyncio.ensure_future(self.mode.run())

    def handle_encoder_change(self, pos):
        self.events.put(messages.EncoderChangeMessage(pos))
        
    def handle_encoder_press(self):
        self.events.put(messages.EncoderPressMessage())
    
    def button_handler(self, button):
        self.events.put(messages.ControllerButtonMessage(button.sname))

    async def controller_monitor(self, poll_time=0.1):
        while True:
            try:
                controller = ControllerResource(dead_zone=0.1, hot_zone=0.2)
            except IOError:
                #no joystick found, wait a bit and try again
                await asyncio.sleep(1.0)
            else:
                with controller as joystick:
                    self.joystick = joystick
                    joystick.buttons.register_button_handler(self.button_handler,
                        list(joystick.buttons.buttons.keys()))
                        
                    self.events.put(messages.ControllerConnectedMessage(True, joystick))
                    while joystick.connected:
                        await asyncio.sleep(poll_time)
                self.events.put(messages.ControllerConnectedMessage(False))
                self.joystick = None
                
    def handle_event(self, event):
        print("Handling event: ", event)
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button =="home":
                self.finished = True
                if self.mode_task:
                    self.mode_task.cancel()
                return True
        return False
                
    async def poll_events(self):
        while True:
            if len(self.events):
                event = self.events.get()
                if self.handle_event(event):
                    pass
                elif self.mode is not None:
                    self.mode.handle_event(event)
            await asyncio.sleep(0.01)

#get up and running...
if __name__=="__main__":
    m = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(m.run())
