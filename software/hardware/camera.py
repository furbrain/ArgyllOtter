#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import scipy.optimize
import asyncio
import time

import calibrate

ISO = 800
RESOLUTION=(640,480)



class CameraPose(calibrate.Settings):
    def default(self):
        self.calibrated = False
        self.degrees_per_pixel = 53.5/640
        self.zero_degree_pixel = 320
        self.distance_params = np.array([100,np.deg2rad(53.5/640.0),240])

    def _get_distance(self, x, h, k, offset):
        return h/np.tan(k*(x+offset))

    def fit_curve(self, y, distance):
        self.distance_params = scipy.optimize.curve_fit(self._get_distance, y, distance, self.distance_params)[0]

    def get_distance(self, y):
        return self._get_distance(y, *self.distance_params)

    def get_bearing(self, x_coord):
        return (x_coord - self.zero_degree_pixel) * self.degrees_per_pixel

    def get_angle_width(self, size):
        return size * self.degrees_per_pixel


class CameraLens(calibrate.Settings):
    def default(self):
        self.mtx = None
        self.dist = None
        self.newmtx = None
        self.roi = None
    
    def set_distortion(self, mtx, dist):
        self.matrix = mtx
        self.dist = dist
        self.newmtx, self.roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (640, 480), 1, (640, 480))

    def undistort_image(self, image):
        if self.mtx is None:
            return image
        dst = cv2.undistort(image, self.mtx, self.dist, None, self.newmtx)

        # crop the image
        x,y,w,h = self.roi
        dst = dst[y:y+h, x:x+w]
        return dst


class Camera:
    def __init__(self, iso=ISO):
        self.camera = PiCamera(framerate=20) 
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.resolution = RESOLUTION
        self.camera.exposure_mode = "auto"
        self.camera.awb_mode = "fluorescent"
        #self.camera.iso = 800
        self.iso = iso
        self.rawCapture = PiRGBArray(self.camera)
        self.pose = CameraPose()
        self.lens = CameraLens()
        

    def set_exposure(self, shutter_speed, awb_gains):
        self.camera.exposure_mode = 'off'
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = awb_gains
        self.camera.shutter_speed = shutter_speed
        
        
    async def get_exposure(self):
        self.camera.iso = self.iso
        self.camera.exposure_mode = "auto"
        self.camera.awb_mode = "auto"
        # Wait for the automatic gain control to settle
        await asyncio.sleep(2)
        # Now return the values
        return (self.camera.exposure_speed, self.camera.awb_gains)

        
    def get_raw_image(self, fast=False):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=fast)
        image = self.rawCapture.array
        return image

        
    def get_image(self, fast=False):
        image = self.get_raw_image(fast)
        return self.lens.undistort_image(image)
                
    def get_position(self, x, y):
        newy = self.pose.get_distance(y)
        angle = self.pose.get_bearing(x)
        newx = newy * np.tan(np.deg2rad(angle))
        return np.array([newx, newy])
        
if __name__=="__main__":
    c = Camera()
    #calibrate()        
    #process()
    c.get_pose()
