#!/usr/bin/env python3

import asyncio
import collections
import os
import traceback
from functools import partial
from PIL import ImageFont

import menu
from modes import messages, shooter, escape, manual, mode
from hardware import Drive, Encoder, Display, Controller, Pixels

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
        self.finished = False
        self.joystick = None
        self.display = Display()
        self.driver = Drive()
        self.encoder = Encoder(self.events)
        self.controller = Controller(self.events)
        self.pixels = Pixels()
        self.menu_items = [
            ("Manual", manual.Manual),
            ("Challenges", [
                ("Shooter", shooter.Shooter),
                ("Escape", [
                    ("Learn", escape.Learn),
                    ("Walk", escape.Walk),
                    ("Run", escape.Run)
                ]),
                ("Lava", None),
                ("Minesweeper", None),
                ("Eco-disaster", None),            
            ]),
            ("Calibrate", None),
            ("STOP", self.driver.stop),
            ("Debug", [
                ("Debug?", self.exit),
                ]),
            ("Shutdown", [
                ("Confirm", self.shutdown),
            ]),
        ]
        self.menu = menu.Menu(self.menu_items, 
                              self.pixels, 
                              self.handle_menu_select_item, 
                              display=self.display)

    async def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.poll_events())
        while not self.finished:
            await asyncio.sleep(0.1)
                   
    async def enter_mode(self, mode):
        if self.mode:
            self.mode.cancel()
        self.pixels.clear()
        self.display.draw_text(mode.__name__)
        try:
            self.mode = mode(self.joystick, self.driver, self.pixels)
            await self.mode.task
        except asyncio.CancelledError:
            pass
        except:
            print("%s raised exception!" % mode.__name__)
            traceback.print_exc()
        finally:
            self.driver.stop()
        self.menu.draw()

            

    def handle_menu_select_item(self, item):
        if item is None: return
        if isinstance(item,type) and issubclass(item, mode.Mode):
            asyncio.ensure_future(self.enter_mode(item))
        else:
            item()

    def exit_mode(self):
        self.driver.stop()
        if self.mode:
            self.mode.cancel()
            self.mode = None
            
    def event_is_exit(self, event):
        if isinstance(event, messages.ControllerButtonMessage) and event.button =="home":
            return True
        if isinstance(event, messages.EncoderPressMessage):
            return True
        return False    
                    
    def handle_event(self, event):
        if isinstance(event, messages.ControllerConnectedMessage):
            self.joystick = event.joystick
            return False #continue processing this event...
        if self.mode is not None:
            if self.event_is_exit(event):
                self.exit_mode()
                return True
        return False
                
    async def poll_events(self):
        while True:
            if len(self.events):
                event = self.events.get()
                if self.handle_event(event):
                    pass
                elif self.mode is None:
                    self.menu.handle_event(event)
                else:
                    self.mode.handle_event(event)
            await asyncio.sleep(0.01)

    def exit(self):
        self.display.clear()
        self.pixels.clear()
        self.finished = True
        
    def shutdown(self):
        self.display.clear()
        self.pixels.clear()
        self.finished = True
        os.system("sudo shutdown -h now")
        
#get up and running...
if __name__=="__main__":
    m = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(m.run())
