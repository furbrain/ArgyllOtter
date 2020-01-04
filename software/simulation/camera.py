#!/usr/bin/env python3

import cv2
import numpy as np
import asyncio
import time
from vtk.util import numpy_support

ISO = 800
class Calibration:
    def __init__(self):
        self.calibrated = False
        self.degrees_per_pixel = 53.5/640.0
        self.zero_degree_pixel = 320

class Camera:
    camera = None
    calibration = Calibration()

    def __init__(self, arena, iso=800):
        self.iso = iso
        self.arena = arena

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
        image = self.arena.get_image()
        rows, cols, _ = image.GetDimensions()
        scalars = image.GetPointData().GetScalars()
        resultingNumpyArray = numpy_support.vtk_to_numpy(scalars)
        resultingNumpyArray = resultingNumpyArray.reshape(cols, rows, -1)
        red, green, blue, alpha = np.dsplit(resultingNumpyArray, resultingNumpyArray.shape[-1])
        resultingNumpyArray = np.stack([blue, green, red, alpha], 2).squeeze()
        resultingNumpyArray = np.flip(resultingNumpyArray, 0)
        return resultingNumpyArray
                
    def get_pose(self):
        raise NotImplemented

