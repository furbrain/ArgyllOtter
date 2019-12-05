#!/usr/bin/env python3

import cv2
import numpy as np
import asyncio
import time

ISO = 800
class Calibration:
    def __init__(self):
        self.calibrated = False
        self.degrees_per_pixel = None
        self.zero_degree_pixel = None

class Camera:
    camera = None
    calibration = Calibration()

    def __init__(self, iso=800):
        self.iso = iso

    def set_exposure(self, shutter_speed, awb_gains):
        pass        
        
    async def get_exposure(self):
        return(10000,(1,1))

    def set_calibration(self, mtx, dist):
        pass
                
    def save_calibration(self):
        pass
        
    def get_raw_image(self):
        raise NotImplemented

    def undistort_image(self, image):
        raise NotImplemented
        
    def get_image(self):
        raise NotImplemented
                
    def get_pose(self):
        raise NotImplemented

