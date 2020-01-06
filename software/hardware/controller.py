import asyncio
from modes import messages
from util import start_task
from approxeng.input.selectbinder import ControllerResource


class Controller:
    def __init__(self, event_queue):
        self.event_queue = event_queue
        start_task(self.monitor())

    def add_event(self, msg):
        self.event_queue.put(msg)

    def button_handler(self, button):
        self.add_event(messages.ControllerButtonMessage(button.sname))

    async def monitor(self, poll_time=0.1):
        while True:
            try:
                controller = ControllerResource(dead_zone=0.05, hot_zone=0.1)
            except IOError:
                #no joystick found, wait a bit and try again
                await asyncio.sleep(1.0)
            else:
                with controller as joystick:
                    joystick.buttons.register_button_handler(self.button_handler,
                        list(joystick.buttons.buttons.keys()))
                        
                    self.add_event(messages.ControllerConnectedMessage(True, joystick))
                    while joystick.connected:
                        await asyncio.sleep(poll_time)
                self.add_event(messages.ControllerConnectedMessage(False))
        
