#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import asyncio
import time

ISO = 800
RESOLUTION=(640,480)

class Calibration:
    def __init__(self):
        self.calibrated = False
        self.degrees_per_pixel = None
        self.zero_degree_pixel = None

class Camera:
    def __init__(self, iso=ISO):
        self.camera = PiCamera(framerate=6) #make camera class level
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.resolution = RESOLUTION
        self.camera.iso = 800
        self.iso = iso
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.iso=self.iso
        self.calibration = Calibration
        try:
            d = np.load("/home/pi/camera_calibration.npz")
            self.set_calibration(d['mtx'], d['dist'])
            d.close()
        except IOError:
            self.cal_mtx = None
            self.cal_dist = None
            self.can_newmtx = None
            self.cal_roi = None

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

    def set_calibration(self, mtx, dist):
        self.cal_mtx = mtx
        self.cal_dist = dist
        self.cal_newmtx, self.cal_roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (640, 480), 1, (640, 480))
        
    def save_calibration(self):
        np.savez("/home/pi/camera_calibration.npz", mtx=self.cal_mtx, dist=self.cal_dist)

    def get_raw_image(self):
        self.rawCapture.truncate(0)
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array
        return image

    def undistort_image(self, image):
        dst = cv2.undistort(image, self.cal_mtx, self.cal_dist, None, self.cal_newmtx)

        # crop the image
        x,y,w,h = self.cal_roi
        dst = dst[y:y+h, x:x+w]
        return dst
        
    def get_image(self):
        image = self.get_raw_image()
        return self.undistort_image(image)
                
    def get_pose(self):
        image = self.get_image()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,7),None)
        cv2.imwrite('in.png', image)
        if ret == True:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            objp = np.zeros((7*9,3), np.float32)
            objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)
            axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

            # Find the rotation and translation vectors.
            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, self.cal_mtx, self.cal_dist)

            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, self.cal_mtx, self.cal_dist)

            image = draw(image,corners2,imgpts)
            cv2.imwrite('out.png', image)
        else:
            print("Fail")

if __name__=="__main__":
    c = Camera()
    #calibrate()        
    #process()
    c.get_pose()
