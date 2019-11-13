#!/usr/bin/env python3
import smbus
import gpiozero
import math
import struct
from . import orientation
import numpy as np
import time
import asyncio
import logging
from util import logged

I2C_ADDRESS = 0x33
ALERT_REGISTER = 0x5F

class Drive:
    def __init__(self, bus=None, wheel_diameter=70.0, clicks_per_revolution=374):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.clicks_per_mm = clicks_per_revolution/(math.pi*wheel_diameter)
        self.orientation = orientation.Orientation(bus=self.bus)
        self.alert = gpiozero.Button(4)
        results = []
        for i in range(20):
            results += [self.orientation.get_rotation()]
            time.sleep(0.02)
        self.gyro_cal = np.mean(results, axis=0)
        self.reset_position()
        self.reset_alert()
        self.get_alert()
        
    def __str__(self):
        return "Drive instance"
        
    def reset_alert(self):
        self.get_alert()
        self.bus.write_i2c_block_data(I2C_ADDRESS, ALERT_REGISTER, [0])
        
    def get_alert(self):
        return self.bus.read_i2c_block_data(I2C_ADDRESS, ALERT_REGISTER, 1)[0]
        
        
    def mm2c(self, *args):
        return [int(x * self.clicks_per_mm) for x in args]
    
    def c2mm(self, *args):
        return [int(x / self.clicks_per_mm) for x in args]
    
    @logged            
    def stop(self):
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, [0])
    
    @logged        
    def drive(self, left, right, soft_start=False):
        args = self.mm2c(left, right) + [soft_start]
        command = struct.pack("<BhhB",1, *args)        
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
    
    @logged    
    def goto(self, max_speed, right, left=None, fast=False):
        if fast:
            cmd = 5
        else:
            cmd = 2
        if left is None:
            left = right
        args = self.mm2c(left, right, max_speed)
        command = struct.pack("<Biih", cmd, *args)
        self.reset_alert()
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    @logged
    def set_powers(self, fr, fl, rr, rl):
        args = fr, fl, rr, rl
        command = struct.pack("<Bhhhh",4, *args)       
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
                    
    @logged
    def get_positions(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x10, 0x10)
        positions = struct.unpack("4i", bytes(data))
        return self.c2mm(*positions)

    @logged
    def reset_position(self):
        data = struct.pack("<4i", 0, 0, 0, 0)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x10, list(data))
    
    @logged    
    async def a_goto(self, max_speed, right, left=None, fast=False):
        self.goto(max_speed, right, left, fast)
        while True:
            await asyncio.sleep(0.05)
            if not self.alert.is_pressed:
                await asyncio.sleep(0.05)
                result = self.get_alert()
                logging.info("a_goto finished")
                self.reset_alert()
                return
    
    @logged                        
    def get_velocities(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x08)
        velocities = struct.unpack("4h", bytes(data))
        return self.c2mm(*velocities)
        
    @logged
    def get_constants(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x30, 0x10)
        p,i,d,ratio = struct.unpack("4f", bytes(data))
        return {'kP':p, 'kI':i, 'kD':d, 'ratio':ratio}
        
    @logged
    def get_powers(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x10)
        powers = struct.unpack("<8h", bytes(data))[4:]
        return powers

    @logged
    def get_currents(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x40, 0x08)
        currents = struct.unpack("4h", bytes(data))
        return [x/1000 for x in currents]
    
    @logged
    def get_voltages(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x50, 0x08)
        peripheral, _, main, _ = struct.unpack("4h", bytes(data))
        peripheral /= 1000.0
        main /= 1000.0
        return (peripheral, main)
    
    @logged    
    async def spin(self, angle, max_speed):
        current_angle = 0
        last_time  = time.time()
        slow_speed = min(max_speed,100)
        slowed = False
        if angle > 0:
            self.drive(max_speed, -max_speed)
        else:
            self.drive(-max_speed, max_speed)
        while True:
            await asyncio.sleep(0.007)
            this_time = time.time()
            rotation = self.orientation.get_rotation()-self.gyro_cal
            rotation = rotation[2]*(this_time-last_time)
            logging.debug("Spin: Rotation: %6f + %6f (%f s)" % (current_angle, rotation, this_time-last_time))
            current_angle += rotation
            last_time = this_time
            if not slowed:
                if abs(current_angle - angle) < 30:
                    logging.debug("Spin: Current angle %f: slowed" % current_angle)
                    if angle > 0:
                        self.drive(slow_speed, -slow_speed)
                    else:
                        self.drive(-slow_speed, slow_speed)
                    slowed = True
            if abs(current_angle) > abs(angle):
                logging.debug("Spin: Current angle %f: stopped" % current_angle)
                break;
        self.stop() #this sometimes is not received, so repeat after a short interval
        time.sleep(0.01)
        self.stop()
            
    @logged    
    async def fast_spin(self, angle, max_speed, differential = 0.333):
        current_angle = 0
        last_time  = time.time()
        if angle > 0:
            self.drive(max_speed, max_speed * differential)
        else:
            self.drive(max_speed * differential, max_speed)
        while True:
            await asyncio.sleep(0.007)
            this_time = time.time()
            rotation = self.orientation.get_rotation()-self.gyro_cal
            rotation = rotation[2]*(this_time-last_time)
            logging.debug("Fast_spin: Rotation: %6f + %6f (%f s)" % (current_angle, rotation, this_time-last_time))
            current_angle += rotation
            last_time = this_time
            if abs(current_angle) > abs(angle):
                logging.info("Fast_spin: Current angle %f: finished" % current_angle)
                break;

    @logged
    async def fast_goto(self, speed, distance):
        self.reset_position()
        await asyncio.sleep(0.03)
        self.drive(speed, speed)
        
        if distance > 0:
            while True:
                await asyncio.sleep(0.05)
                pos = self.get_positions()
                if any(x > 10000 for x in pos):
                    logging.debug("fast_goto: bad position")
                    continue
                if any(x > distance for x in pos):
                    return
        else:
            while True:
                await asyncio.sleep(0.05)
                pos = self.get_positions()
                if any(x < -10000 for x in pos):
                    continue
                if any(x < distance for x in pos):
                    return
                    
if __name__ == "__main__":
    import time
    driver = Drive()
    driver.drive(400,-400)
    last_time = time.time()
    angle = 0
    print("CAL:", driver.gyro_cal)
    for i in range(5000):
        time.sleep(0.007)
        this_time = time.time()
        rotation = driver.orientation.get_rotation()-driver.gyro_cal
        rotation = rotation[2]*(this_time-last_time)
        angle += rotation
        print(rotation, angle, this_time-last_time)
        last_time = this_time
        if angle >=320.0:
            driver.drive(100,-100)
        if angle >=360.0:
            break;
    driver.stop()
    time.sleep(0.5)
    driver.stop()
    exit()
    time.sleep(0.01)
    print(driver.get_positions())
    driver.reset_position()
    print(driver.get_positions())
    time.sleep(0.01)
    driver.stop()
    time.sleep(1)
    driver.goto(1000,500)
    time.sleep(6)
    print(driver.get_positions())
    driver.goto(-1000,500)
    time.sleep(3)
    print(driver.get_positions())
    driver.stop()
