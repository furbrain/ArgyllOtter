#!/usr/bin/env python3
import smbus
import struct
import simple_pid
import servo
import orientation
import gpiozero
import numpy as np

BMP388_ADDRESS = 0x77
UP_CAL_FILE = "/home/pi/calibration_up.np"
DOWN_CAL_FILE = "/home/pi/calibration_down.np"
CAL_RANGE = (-30,70,5)

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
        self.servo = servo.Servo()
        self.position = -10
        #self.orientation = orientation.MPU9250(bus=bus, address=0x69)
        self.pid = simple_pid.PID(0.3, 1.5, 0.0001,
                                  output_limits = (70, 145) , 
                                  sample_time=0.05)
        try:
            f = open(UP_CAL_FILE)
        except IOError:
            rng = range(*CAL_RANGE)
            rv = reversed(rng)
            self.cal_up = np.stack(rng,rng).T
            self.cal_down = np.stack(rv,rv).T
        else:
            with f as f:
                self.cal_up = np.load(f)

    def set_angle(self, angle):
        self.pid.setpoint = angle

    def update(self):
        angle = self.orientation.get_angle()
        output = self.pid(angle)
        self.servo.set_pos(output)
        return (angle, output)
        
    def calibrate(self):
        with open("/home/pi/calibration_up.csv", "w") as f:
            for i in range(-30, 70, 5):
                self.serve.set_pos(i)
                time.sleep(1)
                f.write('{:3d},{:6.2f}'.format(i, self.orientation.get_angle()))
        with open("/home/pi/calibration_down.csv", "w") as f:
            for i in reversed(range(-30, 70, 5)):
                self.serve.set_pos(i)
                time.sleep(1)
                f.write('{:3d},{:6.2f}'.format(i, self.orientation.get_angle()))
                
        
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
                barrel.servo.set_pos(100)
                pointer.on()
            else:
                barrel.servo.set_pos(147)
                pointer.off()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    pump.off()
    pointer.off()
    barrel.servo.off()
    time.sleep(0.5)
