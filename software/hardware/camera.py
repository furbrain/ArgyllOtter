#!/usr/bin/env python3

import asyncio
import threading
import time

import cv2
import numpy as np
import scipy.optimize
# noinspection PyUnresolvedReferences
from picamera import PiCamera
# noinspection PyUnresolvedReferences
from picamera.array import PiRGBArray

import settings

ISO = 800
RESOLUTION = (640, 480)


class MultiLock:
    """This class allows one to use a threading lock in async settings"""

    def __init__(self):
        self._lock = threading.Lock()

    def acquire(self, *args, **kwargs):
        return self._lock.acquire(*args, **kwargs)

    def release(self):
        return self._lock.release()

    def locked(self):
        return self._lock.locked()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._lock.__exit__(exc_type, exc_val, exc_tb)

    async def __aenter__(self):
        while not self._lock.acquire(blocking=False):
            await asyncio.sleep(0.0001)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self._lock.__exit__(exc_type, exc_val, exc_tb)


# noinspection PyAttributeOutsideInit
class CameraPose(settings.Settings):
    def default(self):
        self.calibrated = False
        self.degrees_per_pixel = 53.5 / 640
        self.zero_degree_pixel = 320
        self.distance_params = np.array([100, np.deg2rad(53.5 / 640.0), 240])

    @staticmethod
    def _get_distance(x, h, k, offset):
        return h / np.tan(k * (x + offset))

    def fit_curve(self, y, distance):
        self.distance_params = scipy.optimize.curve_fit(self._get_distance, y, distance, self.distance_params)[0]

    def get_distance(self, y):
        return self._get_distance(y, *self.distance_params)

    def get_bearing(self, x_coord):
        return (x_coord - self.zero_degree_pixel) * self.degrees_per_pixel

    def get_angle_width(self, size):
        return size * self.degrees_per_pixel


# noinspection PyAttributeOutsideInit
class CameraLens(settings.Settings):
    def default(self):
        self.mtx = None
        self.dist = None
        self.new_matrix = None
        self.roi = None

    def set_distortion(self, mtx, dist):
        self.matrix = mtx
        self.dist = dist
        self.new_matrix, self.roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (640, 480), 1, (640, 480))

    def undistort_image(self, image):
        if self.mtx is None:
            return image
        dst = cv2.undistort(image, self.mtx, self.dist, None, self.new_matrix)

        # crop the image
        x, y, w, h = self.roi
        dst = dst[y:y + h, x:x + w]
        return dst


class Recorder(threading.Thread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.lock = MultiLock()
        self.rawCapture = PiRGBArray(self.camera)
        self.terminate = False
        self.timestamp = 0
        self.image = None

    def run(self):
        while not self.terminate:
            self.rawCapture.truncate(0)
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            with self.lock:
                self.image = self.rawCapture.array.copy()
                self.timestamp = time.time()


class Camera:
    def __init__(self, iso=ISO):
        self.camera = PiCamera(framerate=20)
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.resolution = RESOLUTION
        self.camera.exposure_mode = "auto"
        self.camera.awb_mode = "fluorescent"
        # self.camera.iso = 800
        self.iso = iso
        self.pose = CameraPose()
        self.lens = CameraLens()
        self.recorder = None

    def start_recorder(self):
        self.recorder = Recorder(self.camera)
        self.recorder.start()

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
        return self.camera.exposure_speed, self.camera.awb_gains

    async def get_async_image(self, latency=0, undistorted=False):
        start = time.time()
        if self.recorder is None:
            self.start_recorder()
        while True:
            async with self.recorder.lock:
                if self.recorder.timestamp > start - latency:
                    image = self.recorder.image.copy()
                    break
            await asyncio.sleep(0.001)
        if undistorted:
            image = self.lens.undistort_image(image)
        return image

    def get_position(self, x, y):
        new_y = self.pose.get_distance(y)
        angle = self.pose.get_bearing(x)
        new_x = new_y * np.tan(np.deg2rad(angle))
        return np.array([new_x, new_y])

    async def finish(self):
        if self.recorder:
            self.recorder.terminate = True
        while self.recorder.is_alive():
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    c = Camera()
    # calibrate()
    # process()
