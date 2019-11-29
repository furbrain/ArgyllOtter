import numpy as np
import asyncio
import cv2
import imutils

from hardware import Camera, Display, Laser
from modes import mode

class WhiteBalance(mode.Mode):
    def on_start(self):
        self.camera = Camera()
        self.display = Display()
        
    async def run(self):
        # Set ISO to the desired value
        await asyncio.sleep(1)
        shutter, awb = await self.camera.get_exposure()    
        self.camera.set_exposure(shutter, (1,1))
        print(shutter, awb)
        await asyncio.sleep(1)
        self.display.draw_text("Paper!")
        await asyncio.sleep(1)
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
        

class CameraPosition(mode.Mode):
    def on_start(self):
        self.camera = Camera()
        self.display = Display()

    async def run(self):
        # define the list of boundaries
        boundary = ([5, 0, 58], [45, 39, 98])
        hsv_boundary = ([30,80,30],[50,255,255])
        lower = np.array(hsv_boundary[0], dtype = "uint8")
        upper = np.array(hsv_boundary[1], dtype = "uint8")
     
        # find the colors within the specified boundaries and apply
        # the mask
        await asyncio.sleep(2)
        image = self.camera.get_image()
        hvs = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        print(hvs[87,321])
        hvs += np.array([40,0,0], dtype = "uint8")
        print(hvs[87,321])
        hvs[:,:,0] = np.mod(hvs[:,:,0], 180)
        print(hvs[87,321])
        mask = cv2.inRange(hvs, lower, upper)
        
        #get rid of blobs	
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
	        
        output = cv2.bitwise_and(image, image, mask = mask)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        if len(cnts) > 0:
        
	        # find the largest contour in the mask, then use
	        # it to compute the minimum enclosing circle and
	        # centroid
	        c = max(cnts, key=cv2.contourArea)	
	        ((x, y), radius) = cv2.minEnclosingCircle(c)
	        M = cv2.moments(c)
	        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))	
	        
	        if radius > 10:
		        #cv2.circle(output, (int(x), int(y)), int(radius),(0, 255, 255), 2)
		        #cv2.circle(output, center, 5, (0, 0, 255), -1)
		        self.display.draw_text("Found")
	        else:
		        self.display.draw_text("Tiny")
        else:
            self.display.draw_text("Nuffin")
        #disp.write_text("I want nutsssssss",2,4)
        #show image side by side
        cv2.imwrite("in.jpg", np.hstack([image, output]))
        cv2.imwrite("red.jpg", output)
        #cv2.waitKey(0)



class Lens(mode.Mode):
    def on_start(self):
        self.camera = Camera()
        self.display = Display()
        
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

