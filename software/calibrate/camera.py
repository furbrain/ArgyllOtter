import numpy as np
import asyncio
import cv2
import imutils
import math

from modes import mode, messages
from compute import vision
from util import spawn

OBJECT_WIDTH = 68.00 #mm

class WhiteBalance(mode.Interactive):
    HARDWARE = ('camera', 'display')
        
    async def run(self):
        # Set ISO to the desired value
        await asyncio.sleep(1)
        shutter, awb = await self.camera.get_exposure()    
        self.camera.set_exposure(shutter, (1,1))
        print(shutter, awb)
        await asyncio.sleep(1)
        self.display.draw_text("Paper!")
        await self.wait_for_button()
        await asyncio.sleep(0.5)
        self.display.clear()
        image = self.camera.get_image()
        cv2.imwrite("before.jpg", image)
        white = np.average(image[220:260,300:340],axis=(0,1))
        awb = (white[1]/white[0], white[1]/white[2])
        print(white)
        shutter = int(shutter * 255/white[1])
        print(shutter, awb)
        self.camera.set_exposure(shutter, awb)
        await asyncio.sleep(1)
        print(self.camera.camera.exposure_speed, self.camera.camera.awb_gains)
        image = self.camera.get_image()
        cv2.imwrite("after.jpg", image)
        

class CameraPosition(mode.Interactive):
    HARDWARE = ('camera', 'display', 'laser')

    async def run(self):
        self.display.draw_text("Place Object", big=False)
        self.laser.on()
        await self.wait_for_button()
        self.display.clear()
        await asyncio.sleep(1)
        self.laser.off()       
        await asyncio.sleep(2)
        image = self.camera.get_image()
        contour = await spawn(vision.find_biggest_contour(image, "red"))
        if contour is not None:        
	        x_min = min(contour[:,:,0])[0]
	        x_max = max(contour[:,:,0])[0]
	        dist = await self.laser.get_distance(Laser.MEDIUM)
	        cal = self.camera.calibration
	        degrees_subtended = math.atan2(OBJECT_WIDTH,dist)*180/math.pi
	        cal.degrees_per_pixel = degrees_subtended/(x_max-x_min)
	        cal.zero_degree_pixel = (x_min+x_max)/2
	        cal.calibrated = True
        else:
            self.display.draw_text("Nuffin")

class Lens(mode.Mode):
    HARDWARE = ('camera', 'display')
        
    async def run(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((9*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.


        self.display.draw_text("Ready")
        await asyncio.sleep(1.5)

        # grab an image from the camera
        self.display.draw_text("Capturing")
        good = 0
        while good<12:
            await asyncio.sleep(2)
            image = self.camera.get_raw_image()

            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (9,7),None)


            # If found, add object points, image points (after refining them)
            if ret == True:
                good += 1
                self.display.draw_text("%d/12" % good)
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(7,7),(-1,-1),criteria)
                imgpoints.append(corners2)
                
                # Draw and display the corners
                img = cv2.drawChessboardCorners(image, (9,7), corners2,ret)
            else:
                self.display.draw_text("Bad")
                    
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        np.savez("/home/pi/camera_calibration.npz", mtx=mtx, dist=dist)
        self.camera.set_calibration(mtx, dist)
        self.camera.save_calibration()
        self.display.draw_text("Saved")
        await asyncio.sleep(2)

