#!/usr/bin/env python3
import smbus
from . import servo
from . import orientation
import gpiozero
import time
import numpy as np

BMP388_ADDRESS = 0x77
CAL_FILE = "/home/pi/shooter_calibration.npz"
CAL_RANGE = (-10,70,5)

class Pressure:
    def __init__(self, bus = None, address = BMP388_ADDRESS):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.address = address
        self.bus.write_byte_data(self.address,0x1b,0x31)
        self.bus.write_byte_data(self.address,0x1c,0x00)
        self.bus.write_byte_data(self.address,0x1d,0x01)
        
    def get_pressure(self):
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x04, 0x03)
            result = data[0] + data[1]*0x100 + data[2]*0x10000
            result *= 0.016
        except IOError:
            result = None
        return result
        
class Barrel:
    def __init__(self, bus=None):
        self.servo = servo.Servo(inverted=True)
        self.position = -10
        self.orientation = orientation.Orientation(bus=bus, address=0x69)
        self.angle = self.orientation.get_angle()
        try:
            f = np.load(CAL_FILE)
        except IOError:
            rng = range(*CAL_RANGE)
            rv = reversed(rng)
            self.cal_range = np.arange(*CAL_RANGE)
            self.cal_up = self.cal_range[:]
            self.cal_down = self.cal_range[:]
        else:
            with f:
                self.cal_range = f['range']
                self.cal_up = f['up']
                self.cal_down = f['down']

    def set_angle(self, angle):
        cur_angle = self.orientation.get_angle()
        print("Start: ", cur_angle)
        if angle > cur_angle+5:
            self.position = np.interp(angle, self.cal_up, self.cal_range)
            print("Pos: ", self.position)
            self.servo.set_pos(self.position)
            time.sleep(0.3)
            cur_angle = self.orientation.get_angle()
        elif angle < cur_angle-5:
            self.position = np.interp(angle, self.cal_down, self.cal_range)
            print("Pos: ", self.position)
            self.servo.set_pos(self.position)
            time.sleep(0.3)
            cur_angle = self.orientation.get_angle()
        print("After first move: ", cur_angle)
        on_pos_count = 0
        while True:
            if (abs(angle-cur_angle)<0.5):
                on_pos_count += 1
                if on_pos_count >=2:
                   break
            else:
                on_pos_count = 0
                if angle<cur_angle:
                   self.position -= 1
                else:
                    self.position += 1
                print("Pos: ", self.position)
                self.servo.set_pos(self.position)
            time.sleep(0.1)
            cur_angle = self.orientation.get_angle()
            print("Incremental: ", cur_angle)
            
    def calibrate(self):
        rng = np.arange(*CAL_RANGE)
        up = []
        down = []
        for i in rng:
            self.servo.set_pos(i)
            time.sleep(1)
            up.append(self.orientation.get_angle())
        for i in reversed(rng):
            self.servo.set_pos(i)
            time.sleep(1)
            down.append(self.orientation.get_angle())
        down = down[::-1]
        np.savez(CAL_FILE, range=rng, up=up, down=down)             
        
def Pointer():
    return gpiozero.LED(22)
    
def Pump():
    return gpiozero.LED(27)
                        
if __name__ == "__main__":
    import time
    barrel = Barrel()
    pressure = Pressure()
    pump = Pump()
    pump.on()
    pointer = Pointer()
    try:
        for i in range(1000):
            air = pressure.get_pressure()
            if  air is not None and air < 100000:
                barrel.servo.set_pos(40)
                pointer.on()
            else:
                barrel.servo.set_pos(-10)
                pointer.off()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    pump.off()
    pointer.off()
    time.sleep(0.5)
