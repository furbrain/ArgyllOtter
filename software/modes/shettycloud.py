#!/usr/bin/python3
import asyncio

import numpy as np
import pygame
import scipy.stats as stats

from util import get_coeffs

# errors are +/- ERROR corresponds to 95 % CIs
START_POS_ERROR = 10
START_AZ_ERROR = 5
SWARM_SIZE = 200
TURN_ERROR = 6
DISTANCE_ERROR = 100
AXIS_OFFSET = -150
AXIS_BEARING = 0
DEBUG_AXIS_BEARING = 0
DEBUG_AXIS_OFFSET = -150

CAMERA_ANGLE_ERROR = 2
CAMERA_DISTANCE_ERROR = 80

WEIGHT_MOVEMENT = True


def draw_cross(surface, colour, pos, size, width=1):
    x = pos[0]
    y = pos[1]
    colour = pygame.Color(colour)
    pygame.draw.line(surface, colour, [x - size, y - size], [x + size, y + size], width)
    pygame.draw.line(surface, colour, [x - size, y + size], [x + size, y - size], width)


class Shetty:
    """
    This represents the robot
    You can tell it to move or turn
    You can tell it a distance and or angle to some feature
    It will keep track of where it is and update itself as needed
    """

    TURN_SPEED = 400
    DRIVE_SPEED = 600

    TURN_RADIUS = 0

    def __init__(self, pos, azimuth, drive):
        self.drive = drive
        self.cloud = ShettyCloud(pos, azimuth)
        self.debug = False

    @property
    def pos(self):
        return self.cloud.get_pos()

    @property
    def azimuth(self):
        return self.cloud.get_azimuth()

    async def turn(self, angle, speed=TURN_SPEED):
        true_angle = await self.drive.spin(angle, speed, accurate=True)
        self.correct_position(true_angle)
        await asyncio.sleep(0.1)

    async def turn_to_azimuth(self, azimuth):
        azimuth %= 360
        turn = azimuth - self.azimuth
        if turn < -180:
            turn = turn + 360
        if turn > 180:
            turn = turn - 360
        await self.turn(turn)

    def correct_position(self, angle):
        if self.debug:
            bearing_adjust = DEBUG_AXIS_BEARING
            offset = DEBUG_AXIS_OFFSET
        else:
            bearing_adjust = AXIS_BEARING
            offset = AXIS_OFFSET

        self.cloud.turn(bearing_adjust, error=0)  # axis of rotation is about 7 cm 45 degrees to rigth behind camera
        self.cloud.move(offset, error=0)
        self.cloud.turn(angle)
        self.cloud.move(-offset, error=0)
        self.cloud.turn(-bearing_adjust, error=0)
        self.cloud.adjust_pos(0)  # add some x/y error in here

    async def move(self, distance, speed=DRIVE_SPEED):
        distance = await self.drive.a_goto(speed, distance, accurate=True)
        self.cloud.move(distance)
        await asyncio.sleep(0.1)

    def get_azimuth_and_distance_to(self, pos):
        if self.debug:
            bearing_adjust = DEBUG_AXIS_BEARING
            offset = DEBUG_AXIS_OFFSET
        else:
            bearing_adjust = AXIS_BEARING
            offset = AXIS_OFFSET
        bearing = self.azimuth + bearing_adjust
        axis = self.pos + get_coeffs(bearing) * offset
        offset = pos - axis
        hypot = np.hypot(*(pos - axis))
        bearing = np.rad2deg(np.arctan2(offset[0], offset[1]))
        o = self.TURN_RADIUS
        extra = np.rad2deg(np.sin(o / hypot))
        distance = np.sqrt(hypot * hypot - o * o)
        return bearing + extra, distance - 150

    def observed(self, angle, pos, distance=None):
        self.cloud.observation(angle, pos, distance)

    def draw(self, arena):
        self.debug = True
        self.cloud.draw(arena)


class ShettyCloud:
    """
    This reperesents a monte carlo particle filter of Shetty's
    it has three main variables: azimuth, xy and weight
    xy refers to the camera position (not centre as previously)
    """

    def __init__(self, pos, azimuth):
        self.dtype = np.dtype([('azimuth', 'float64'), ('xy', 'float64', (2,)), ('weight', 'float64')])
        temp_swarm = np.zeros(SWARM_SIZE, dtype=self.dtype)
        temp_swarm['xy'] = np.random.normal(pos, START_POS_ERROR / 2, (SWARM_SIZE, 2))
        temp_swarm['azimuth'] = np.random.normal(azimuth, START_AZ_ERROR / 2, (SWARM_SIZE))
        temp_swarm['weight'] = np.ones((SWARM_SIZE))
        self.swarm = temp_swarm.view(np.recarray)
        self.dirty = True

    def wrap_azimuth(self):
        self.swarm.azimuth %= 360

    def normalize_weights(self):
        self.swarm.weight[np.isnan(self.swarm.weight)] = 0
        if np.sum(self.swarm.weight)==0:
            self.swarm.weight = np.ones_like(self.swarm.weight)
        self.swarm.weight /= np.sum(self.swarm.weight)

    def resample(self):
        self.normalize_weights()
        Ninv = 1 / SWARM_SIZE
        new_swarm = np.zeros(SWARM_SIZE, dtype=self.dtype)
        r = np.random.uniform(0, Ninv)
        # weight
        c = self.swarm.weight[0]
        i = 0
        for j in range(0, SWARM_SIZE):
            # Or j-1 if out of range
            U = r + (j) * Ninv
            while U > c:
                i = i + 1
                c = c + self.swarm.weight[i]
            new_swarm[j] = self.swarm[i]
        self.swarm = new_swarm.view(np.recarray)
        self.dirty = True

    def get_bearing_to_pos(self, pos):
        offsets = pos - self.swarm.xy
        bearings = np.rad2deg(np.arctan2(offsets[:, 0], offsets[:, 1]))
        bearings -= self.swarm.azimuth
        bearings %= 360
        return bearings

    def get_distance_to_pos(self, pos):
        offsets = pos - self.swarm.xy
        distances = np.hypot(offsets[:, 0], offsets[:, 1])
        return distances

    def observation(self, angle, pos, distance):
        """the camera has seen feature at known pos, with given angle"""
        print("observation: ", self.get_pos(), angle, pos)
        print("current:", self.get_azimuth())
        bearings = self.get_bearing_to_pos(pos)
        error = bearings - angle
        # convert to  interval of -180 -> +180
        error[error > 180] -= 360
        error[error < -180] += 360
        weighting = stats.norm.pdf(error, scale=CAMERA_ANGLE_ERROR)
        self.swarm.weight *= weighting
        if distance is not None:
            error = self.get_distance_to_pos(pos) - distance
            weighting = stats.norm.pdf(error, scale=CAMERA_DISTANCE_ERROR)
            self.swarm.weight *= weighting
        self.normalize_weights()
        self.dirty = True
        print("after: ", self.get_azimuth())

    def turn(self, angle, error=TURN_ERROR):
        self.resample()
        self.swarm.azimuth += angle
        if error != 0:
            offset = np.random.normal(0, error / 2, SWARM_SIZE)
            if WEIGHT_MOVEMENT:
                weighting = stats.norm.pdf(offset, scale=error / 2)
            else:
                weighting = 1
            self.swarm.azimuth += offset
            self.swarm.weight *= weighting
        self.wrap_azimuth()
        self.normalize_weights()
        self.dirty = True

    def move(self, distance, error=DISTANCE_ERROR):
        self.resample()
        coeff = get_coeffs(self.swarm.azimuth)
        if error != 0:
            offset = np.random.normal(distance, error / 2, SWARM_SIZE)
            if WEIGHT_MOVEMENT:
                weighting = stats.norm.pdf(offset, loc=distance, scale=error / 2)
            else:
                weighting = 1
            distance = offset
        else:
            weighting = 1
        offsets = coeff * distance
        self.swarm.xy += offsets.T
        self.swarm.weight *= weighting
        self.normalize_weights()
        self.dirty = True

    def adjust_pos(self, offset, error=DISTANCE_ERROR):
        self.resample()
        error = np.random.normal(0, error / 2, (SWARM_SIZE, 2))
        self.swarm.xy += offset
        self.swarm.xy += error
        self.dirty = True

    def calc_pos_and_azimuth(self):
        self.pos = np.average(self.swarm.xy, weights=self.swarm.weight, axis=0)
        if max(self.swarm.azimuth) - min(self.swarm.azimuth) > 180:
            rotated = (self.swarm.azimuth + 180) % 360
            result = np.average(rotated, weights=self.swarm.weight)
            self.azimuth = (result - 180) % 360
        else:
            self.azimuth = np.average(self.swarm.azimuth, weights=self.swarm.weight)
        self.dirty = False

    def get_pos(self):
        if self.dirty:
            self.calc_pos_and_azimuth()
        return self.pos

    def get_azimuth(self):
        if self.dirty:
            self.calc_pos_and_azimuth()
        return self.azimuth

    def draw(self, arena):
        height = arena.screen.get_height()
        for pos in self.swarm.xy:
            pt = [int(x * arena.SCALE) for x in pos]
            pt[1] = height - pt[1]
            arena.screen.set_at(pt, (255, 255, 255))
        pt = arena.coords(self.get_pos())
        direction = self.get_pos() + 300 * get_coeffs(self.azimuth)
        direction = arena.coords(direction)
        draw_cross(arena.screen, "white", pt, 15)
        pygame.draw.line(arena.screen, (255, 255, 255), pt, direction)


if __name__ == "__main__":
    s = ShettyCloud((1100, 400), 0)
    s.turn(90)
    s.move(100)
    s.turn(-90)
    s.move(100)
    s.turn(-90)
    s.move(100)
    s.turn(90)

    s.observation(0.0, np.array((1100, 2200)), None)
    s.observation(90.0, np.array((1800, 500)), None)
    s.turn(10)
    print(np.average(s.swarm.xy, axis=0))
    print(np.average(s.swarm.xy, weights=s.swarm.weight, axis=0))

    print(np.average(s.swarm.azimuth))
    print(np.average(s.swarm.azimuth, weights=s.swarm.weight))
