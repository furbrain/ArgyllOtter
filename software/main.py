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
        self.queue = DiscardingQueue(20)
        #set up controller if present

    async def run(self):
        #set up encoder
        loop = asyncio.get_event_loop()
        #encoder = hardware.Encoder((19,13,26), self.handle_encoder_change, self.handle_encoder_press)
        loop.create_task(self.controller_monitor())
        loop.create_task(self.handle_events())
        await asyncio.sleep(10)

    def handle_encoder_change(self, pos):
        self.queue.put(messages.EncoderChangeMessage(pos))
        
    def handle_encoder_press(self):
        self.queue.put(messages.EncoderPressMessage())

    async def controller_monitor(self, poll_time=0.1):
        while True:
            try:
                controller = ControllerResource(dead_zone=0.1, hot_zone=0.2)
            except IOError:
                #no joystick found, wait a bit and try again
                await asyncio.sleep(1.0)
            else:
                with controller as joystick:
                    self.queue.put(messages.ControllerConnectedMessage(True))
                    while joystick.connected:
                        self.queue.put(messages.ControllerAxisMessage('left', *joystick['lx', 'ly']))
                        self.queue.put(messages.ControllerAxisMessage('right', *joystick['rx', 'ry']))
                        joystick.check_presses()
                        for press in joystick.presses:
                            self.queue.put(messages.ControllerButtonMessage(press))
                        await asyncio.sleep(poll_time)
                queue.put(messages.ControllerConnectedMessage(False))
                
    async def handle_events(self):
        while True:
            if len(self.queue):
                print(self.queue.get())
            await asyncio.sleep(0.01)

#get up and running...
m = Main()
loop = asyncio.get_event_loop()
loop.run_until_complete(m.run())
