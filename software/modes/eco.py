from modes import mode
from hardware import Camera, Display, Laser, Grabber
import numpy as np
import asyncio
import cv2
import imutils


class Retrieve(mode.Mode):
    def on_start(self):
        self.camera = Camera()
        self.display = Display()
        self.laser = Laser()
        self.grabber = Grabber()

    async def run(self):
        self.grabber.open()
        # define the list of boundaries
        boundary = ([5, 0, 58], [45, 39, 98])
        hsv_boundary = ([30,80,30],[50,255,255])
        lower = np.array(hsv_boundary[0], dtype = "uint8")
        upper = np.array(hsv_boundary[1], dtype = "uint8")
     
        # find the colors within the specified boundaries and apply
        # the mask
        await asyncio.sleep(1)
        image = self.camera.get_image()
        hvs = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #monkeying about to bring red into middle of colour space
        hvs += np.array([40,0,0], dtype = "uint8")
        hvs[:,:,0] = np.mod(hvs[:,:,0], 180)
        mask = cv2.inRange(hvs, lower, upper)
        
        #get rid of blobs	
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
	        
        output = cv2.bitwise_and(image, image, mask = mask)
        
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        if len(cnts) > 0:
        
	        # find the largest contour in the mask, then use
	        # it to compute the minimum enclosing circle and
	        # centroid
	        c = max(cnts, key=cv2.contourArea)
	        print(c)
	        print(c.shape)
	        x_min = min(c[:,:,0])[0]
	        x_max = max(c[:,:,0])[0]
	        y_max = max(c[:,:,1])[0]
	        pos = (x_min+x_max/2) - self.camera.calibration.zero_degree_pixel
	        angle = pos * self.camera.calibration.degrees_per_pixel
	        await self.drive.spin(angle, 100)
	        dist = await self.laser.get_distance(Laser.MEDIUM)
	        await self.drive.a_goto(200,dist-10)
	        self.grabber.close()
	        await asyncio.sleep(0.6)
	        await self.drive.a_goto(200,-dist)
	        self.grabber.open()
	        await asyncio.sleep(0.6)
        else:
            self.display.draw_text("Nuffin")
        cv2.imwrite("in.jpg", np.hstack([image, output]))
        self.grabber.off()
