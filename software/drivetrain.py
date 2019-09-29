#!/usr/bin/env python3
import smbus
import math
import struct

I2C_ADDRESS = 0x33

class DriveTrain:
    def __init__(self, bus=None, wheel_diameter=70.0, clicks_per_revolution=374):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.clicks_per_mm = clicks_per_revolution/(math.pi*wheel_diameter)
        
    def mm2c(self, *args):
        return [int(x * self.clicks_per_mm) for x in args]
    
    def c2mm(self, *args):
        return [int(x / self.clicks_per_mm) for x in args]
                
    def stop(self):
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, [0])
            
    def drive(self, left, right):
        args = self.mm2c(left, right)
        command = struct.pack("<Bhh",1, *args)        
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
        
    def goto(self, left, right, max_speed):
        args = self.mm2c(left, right, max_speed)
        command = struct.pack("<Biih", 2, *args)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    def individual(self, fr, fl, rr, rl):
        args = self.mm2c(fr, fl, rr, rl)
        command = struct.pack("<Bhhhh",4, *args)       
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
                    
    def get_positions(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x10, 0x10)
        positions = struct.unpack("4i", bytes(data))
        return self.c2mm(*positions)
        
    def get_velocities(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x08)
        velocities = struct.unpack("4h", bytes(data))
        return self.c2mm(*velocities)

    def get_constants(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x30, 0x10)
        p,i,d,ratio = struct.unpack("4f", bytes(data))
        return {'kP':p, 'kI':i, 'kD':d, 'ratio':ratio}

    def get_currents(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x40, 0x08)
        currents = struct.unpack("4h", bytes(data))
        return [x/1000 for x in currents]
    
    def get_voltages(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x50, 0x08)
        peripheral, _, main, _ = struct.unpack("4h", bytes(data))
        peripheral /= 1000.0
        main /= 1000.0
        return (peripheral, main)
    
if __name__ == "__main__":
    import time
    driver = DriveTrain()
    time.sleep(0.01)
    print(driver.get_positions())
    time.sleep(0.01)
    driver.stop()
    time.sleep(1)
    driver.goto(1000,1000,500)
    time.sleep(6)
    print(driver.get_positions())
    driver.goto(000,000,500)
    time.sleep(3)
    print(driver.get_positions())
    driver.stop()
