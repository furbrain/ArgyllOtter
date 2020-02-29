#!/usr/bin/env python3

import asyncio

import numpy as np
from vtk.util import numpy_support

ISO = 800


class Calibration:
    def __init__(self):
        self.calibrated = False
        self.degrees_per_pixel = 56 / 640.0
        self.zero_degree_pixel = 320

    def get_bearing(self, x_coord):
        return (x_coord - self.zero_degree_pixel) * self.degrees_per_pixel

    def get_angle_width(self, size):
        return size * self.degrees_per_pixel


class Camera:

    def __init__(self, arena, iso=800):
        self.iso = iso
        self.arena = arena
        self.pose = Calibration()

    def set_exposure(self, shutter_speed, awb_gains):
        pass

    async def get_exposure(self):
        return (10000, (1, 1))

    def set_calibration(self, mtx, dist):
        pass

    def save_calibration(self):
        pass

    def get_raw_image(self):
        raise NotImplemented

    def undistort_image(self, image):
        raise NotImplemented

    async def a_get_image(self):
        image = self.get_image()
        await asyncio.sleep(0.15)
        return image

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

    def get_position(self, x, y):
        y = 240 - y
        angle = -y * self.pose.degrees_per_pixel
        print("angle", angle)
        height = 100
        newy = height / np.tan(np.deg2rad(angle))
        x = x - self.pose.zero_degree_pixel
        print(x, y)
        angle = x * self.pose.degrees_per_pixel
        print("angle", angle)
        newx = newy * np.tan(np.deg2rad(angle))
        return np.array([newx, newy])
