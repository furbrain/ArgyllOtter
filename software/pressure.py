#!/usr/bin/env python3
import smbus
import struct

BMP388_ADDRESS = 0x77

class BMP388:
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
        data = self.bus.read_i2c_block_data(self.address, 0x04, 0x03)
        result = data[0] + data[1]*0x100 + data[2]*0x10000
        result *= 0.016
        return result
        
if __name__ == "__main__":
    import time
    p = BMP388()
    for x in range(100):
         time.sleep(0.5)
         print(p.get_pressure())
