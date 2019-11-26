#!/usr/bin/env python3

import asyncio
import collections
import os
from functools import partial

import menu
from modes import messages, shooter, escape, manual, mode
from approxeng.input.selectbinder import ControllerResource
from hardware import Drive, Encoder, Display



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
        self.joystick = None
        self.display = Display()
        self.driver = Drive()
        self.encoder = Encoder(self.handle_encoder_change, self.handle_encoder_press)
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
                ("Confirm",partial(os.system, "sudo shutdown -h now")),
            ]),
        ]
        self.menu = menu.Menu(self.menu_items, self.handle_menu_select_item, display=self.display)

    async def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.controller_monitor())
        loop.create_task(self.poll_events())
        while not self.finished:
            await asyncio.sleep(0.1)
            
    def manage_mode_finished(self, task):
        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print("Mode raised exception!")
            print(type(e), e)
            self.driver.stop()
            raise e
        self.menu.draw()    
            
       
    def enter_mode(self, mode):
        if self.mode_task:
            self.mode_task.cancel()
        self.display.clear()
        self.mode = mode(self.joystick, self.driver, None) #FIXME replace None with neopixel instance
        self.mode_task = asyncio.ensure_future(self.mode.run())
        self.mode_task.add_done_callback(self.manage_mode_finished)

    def handle_encoder_change(self, pos):
        self.events.put(messages.EncoderChangeMessage(pos))
        
    def handle_encoder_press(self):
        self.events.put(messages.EncoderPressMessage())

    def handle_menu_select_item(self, item):
        if item is None: return
        if isinstance(item,type) and issubclass(item, mode.Mode):
            self.enter_mode(item)
        else:
            item()
    
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

    def exit_mode(self):
        self.driver.stop()
        if self.mode_task:
            self.mode_task.cancel()
            self.mode_task = None
            self.mode = None
        self.menu.draw()
                    
    def handle_event(self, event):
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button =="home":
                self.exit_mode()
                return True
        if self.mode is None:
            if isinstance(event, messages.ControllerButtonMessage):
                if event.button == "dup":
                    self.menu.item_changed(False)
                    return True
                elif event.button == "ddown":
                    self.menu.item_changed(True)
                    return True
                elif event.button == "start":
                    self.menu.item_selected()
                    return True
            elif isinstance(event, messages.EncoderChangeMessage):
                if self.mode is None:
                    self.menu.item_changed(event.pos)
                    return True
            elif isinstance(event, messages.EncoderPressMessage):
                if self.mode is None:
                    self.menu.item_selected()
                else:
                    self.exit_mode()
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

    def exit(self):
        self.display.clear()
        self.finished = True
        
#get up and running...
if __name__=="__main__":
    m = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(m.run())
