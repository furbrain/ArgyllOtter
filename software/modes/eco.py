from modes import mode
from hardware import Camera, Display, Laser, Grabber
import asyncio
from compute import vision


class Retrieve(mode.Mode):
    def on_start(self):
        self.camera = Camera()
        self.display = Display()
        self.laser = Laser()
        self.grabber = Grabber()

    async def run(self):
        self.grabber.open()
        await asyncio.sleep(1)
        image = self.camera.get_image()
        contour = await spawn(vision.find_biggest_contour(image, colour_name="red"))
        if contour is not None:
        
	        # find the largest contour in the mask, then use
	        # it to compute the minimum enclosing circle and
	        # centroid
	        x_min = min(contour[:,:,0])[0]
	        x_max = max(contour[:,:,0])[0]
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
        self.grabber.off()
