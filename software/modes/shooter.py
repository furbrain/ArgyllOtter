#!/usr/bin/env python3
from . import manual, messages
import hardware
import asyncio
import time

class Shooter(manual.Manual):
    def __init__(self, joystick):
        super().__init__(joystick)
        self.barrel = hardware.Barrel()
        self.pressure = hardware.Pressure()
        self.pump = hardware.Pump()
        self.pointer = hardware.Pointer()
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
        self.state_task = asyncio.ensure_future(state())
        
    def handle_event(self, event):
        if isinstance(event, messages.ControllerButtonMessage):
            if event.button == "cross":
                if self.aimable:
                    self.set_state(self.Fire)
            elif event.button == "triangle":
                self.set_state(self.Load)
            elif event.button == "circle":
                self.set_state(self.Off)
            elif event.button == "square":
                self.set_state(self.Reload)

    async def EngageBall(self):
        self.pump.on()
        while True:
            await asyncio.sleep(0.03)
            if (self.pressure.get_pressure() < 100000):
                self.pump.off()
                break

    async def Load(self):
        self.pump.off()
        self.pointer.off()
        self.barrel.set_angle_quick(-20)
        await asyncio.sleep(0.3)
        try:
            await asyncio.wait_for(self.EngageBall(),2.0)
        except asyncio.TimeoutError:
            #ball not engaged...
            self.pump.off()
            self.barrel.set_angle_quick(20)
            await asyncio.sleep(0.3)
            #start again...
            self.set_state(self.Load)
        else:    
            #ball in correct position, move on to Aim mode
            self.pump.off()
            self.set_state(self.Aim)
        
    async def Aim(self):
        angle_task = asyncio.ensure_future(self.barrel.set_angle(self.angle))
        self.pointer.on()
        while True:
            await asyncio.sleep(0.1)
            if (self.pressure.get_pressure() > 105000):
                self.pump.on()
            else:
                self.pump.off()
            if angle_task and angle_task.done():
                self.aimable=True
                self.angle = self.barrel.get_pos()
                angle_task = None
                
    async def Fire(self):
        self.angle = self.barrel.getAngle()
        self.aimable = False
        self.pump.on()
        self.pointer.off()
        while True:
            await asyncio.sleep(0.1)
            if (self.pressure.get_pressure() > 108000):
                asyncio.ensure_future(self.Load())
                break
    
    async def Off(self):
        self.pointer.off()
        self.pump.off()
        self.barrel.set_angle_quick(-20)
        await asyncio.sleep(0.3)
        self.barrel.servo.off()
        
    async def Reload(self):
        self.pointer.off()
        self.pump.off()
        self.barrel.set_angle_quick(60)
        
    async def run(self):
        asyncio.ensure_future(super().run())
        self.set_state(self.Off)
        while True:
            if self.joystick and self.joystick.connected:
                if self.aimable:
                    y = self.joystick['ry']
                    if y != 0.0:
                        self.angle += y*2.0
                        print("Angle = ", self.angle)
                        self.barrel.set_pos(self.angle)                    
            await asyncio.sleep(0.1)    
