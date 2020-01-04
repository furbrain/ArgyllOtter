#!/usr/bin/env python3
from . import manual, messages
import asyncio
import time
from util import start_task

class Shooter(manual.Manual):
    HARDWARE = ('drive', 'shooter', 'laser')
    def on_start(self):
        super().on_start()
        self.angle = 0
        self.state = None
        self.state_task = None
        self.aimable = False
        self.set_state(self.Off)
        print("Shooter initialised")
        
    def set_state(self, state):
        print("Setting state to ", state.__name__)
        if self.state_task is not None:
            self.state_task.cancel()
        self.state = state
        self.state_task = start_task(state())
        
    def handle_event(self, event):
        if super().handle_event(event):
            return True
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button == "triangle":
                self.set_state(self.Load)
            elif event.button == "circle":
                self.set_state(self.Off)
            elif event.button == "square":
                self.set_state(self.Reload)
            if self.aimable:
                if event.button == "dup":
                    self.angle += 2
                    self.shooter.barrel.set_pos(self.angle)                    
                elif event.button == "ddown":
                    self.angle -= 2
                    self.shooter.barrel.set_pos(self.angle)                    
                elif event.button == "cross":
                    self.set_state(self.Fire)

    async def EngageBall(self):
        self.shooter.pump.on()
        while True:
            await asyncio.sleep(0.03)
            if (self.shooter.pressure.get_pressure() < 100000):
                self.shooter.pump.off()
                break

    async def Load(self):
        self.shooter.pump.off()
        self.shooter.pointer.off()
        self.shooter.barrel.set_angle_quick(-20)
        await asyncio.sleep(0.3)
        try:
            await asyncio.wait_for(self.EngageBall(),2.0)
        except asyncio.TimeoutError:
            #ball not engaged...
            self.shooter.pump.off()
            self.shooter.barrel.set_angle_quick(20)
            await asyncio.sleep(0.3)
            #start again...
            self.set_state(self.Load)
        else:    
            #ball in correct position, move on to Aim mode
            self.shooter.pump.off()
            self.set_state(self.Aim)
        
    async def Aim(self):
        angle_task = start_task(
                         asyncio.wait_for(
                             self.shooter.barrel.set_angle(self.angle),2.0))
        while True:
            await asyncio.sleep(0.1)
            if (self.shooter.pressure.get_pressure() > 105000):
                self.shooter.pump.on()
            else:
                self.shooter.pump.off()
            if angle_task and angle_task.done():
                try:
                    angle_task.result()
                except asyncio.TimeoutError:
                    pass
                self.shooter.pointer.on()
                self.aimable=True
                self.angle = self.shooter.barrel.get_pos()
                angle_task = None
                
    async def Fire(self):
        self.angle = self.shooter.barrel.getAngle()
        self.aimable = False
        self.shooter.pump.on()
        self.shooter.pointer.off()
        #FIXME create firing solution here and implement it
        while True:
            await asyncio.sleep(0.1)
            if (self.shooter.pressure.get_pressure() > 108000):
                start_task(self.Load())
                break
    
    async def Off(self):
        self.shooter.pointer.off()
        self.shooter.pump.off()
        self.shooter.barrel.set_angle_quick(-20)
        await asyncio.sleep(0.3)
        self.shooter.barrel.servo.off()
        
    async def Reload(self):
        self.shooter.pointer.off()
        self.shooter.pump.off()
        self.shooter.barrel.set_angle_quick(60)
        
    async def run(self):
        start_task(super().run())
        self.set_state(self.Off)
        while True:
            if self.joystick and self.joystick.connected:
                if self.aimable:
                    y = self.joystick['ry']
                    if y != 0.0:
                        self.angle += y*20.0
                        print("Angle = ", self.angle)
                        self.shooter.barrel.set_pos(self.angle)                    
            await asyncio.sleep(0.1)    
