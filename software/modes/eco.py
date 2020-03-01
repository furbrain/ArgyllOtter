import asyncio

import numpy as np
import pygame

from modes import mode
from util import logged
from . import eye
from .barrels import Barrel, BarrelMap
from .shettycloud import Shetty

TURN_SPEED = 400
MIN_TURN_SPEED = 150
DRIVE_SPEED = 800


# FIXME
# so there are two problems
# one is we get lost and don't correctly navigate to the final zones
# could we put a higher laser range finder to measure distance accurately to end zones?
# and focus in on end zones during final part of route finding...
# note we aren't using the lower range finder at all now...

# second is we seem to lose green barrels, even when pointing directly at them?
# let's check the range and relative azimuths of what we get out

def draw_cross(surface, colour, pos, size, width=1):
    x = pos[0]
    y = pos[1]
    colour = pygame.Color(colour)
    pygame.draw.line(surface, colour, [x - size, y - size], [x + size, y + size], width)
    pygame.draw.line(surface, colour, [x - size, y + size], [x + size, y - size], width)


def angle_over(target, angle):
    while target > angle:
        angle += 360
    if angle < target + 90:
        return True
    return False


class EcoDisaster(mode.Mode):
    HARDWARE = ('drive', 'camera', 'laser', 'grabber', 'display', 'stabber', 'pixels')

    def on_start(self):
        self.barrel_map = BarrelMap()
        self.shetty = Shetty(np.array((1100, 550)), 0, self.drive)
        self.eyeball = eye.Ball(self.camera, self.shetty, self.barrel_map)
        self.route = []
        self.red_count = 0
        self.green_count = 0

    def update_pixels(self):
        self.pixels.clear()
        #for i in range(self.barrel_map.count("red")):
        #    self.pixels.setPixelColorRGB(i, 80, 0, 0)
        #for i in range(self.barrel_map.count("green")):
        #    self.pixels.setPixelColorRGB(11 - i, 0, 80, 0)
        #self.pixels.show()
        #for c in "red", "green":
        #    print(c, self.barrel_map.count(c))

    async def get_distance(self):
        for i in range(3):
            try:
                dist = await self.laser.get_distance(speed=self.laser.FAST)
            except (self.laser.BadReadingError, self.laser.TimeoutError) as e:
                print("Laser error: ", e)
                continue
            if dist < 10000:
                return dist
            print("distance too far")
        return None

    @logged
    async def fine_tune_laser(self, barrel):
        speed = TURN_SPEED / 2
        with self.stabber:
            while True:
                adjustment = await self.eyeball.line_up_for_laser(barrel)
                if adjustment is None:
                    return False
                if abs(adjustment) < 1:
                    return True
                self.stabber.stab()
                await asyncio.sleep(0.1)
                await self.shetty.turn(adjustment, speed=speed)
                speed = max(speed / 2, MIN_TURN_SPEED)

    async def fine_tune_grab(self, barrel):
        speed = TURN_SPEED / 2
        with self.stabber:
            for i in range(5):
                adjustment, target = await self.eyeball.line_up_for_grab(barrel)
                if adjustment is None:
                    return False, None
                if abs(adjustment) < 5:
                    return True, target
                if target.get_distance(self.shetty.pos) < 200:
                    return True, target
                self.stabber.stab()
                await asyncio.sleep(0.1)
                await self.shetty.turn(adjustment, speed=speed)
                speed = max(speed / 2, MIN_TURN_SPEED)
        return True, target

    async def pinpoint_barrel(self, barrel):
        angle, _ = self.shetty.get_azimuth_and_distance_to(barrel.pos)
        with self.stabber.stab():
            await self.shetty.turn_to_azimuth(angle)
            found = await self.fine_tune_laser(barrel)
            if found:
                distance = await self.get_distance()
                if distance is None:
                    return barrel
                precise_barrel = Barrel.fromPolar(self.shetty.pos, self.shetty.azimuth, distance, barrel.colour)
                if barrel.near(precise_barrel):
                    return precise_barrel
                else:  # oops, probably another barrel in the way or we just missed with the laser
                    return barrel  # use position from camera
            return None

    @logged
    async def create_map(self, start_angle, finish_angle):
        self.display.draw_text("Mapping")
        # find most leftward barrels
        with self.stabber.stab():
            await self.shetty.turn_to_azimuth(start_angle)
            while not angle_over(finish_angle, self.shetty.azimuth):
                known, unknown = await self.eyeball.find_and_classify_barrels()
                for barrel in unknown:
                    if barrel.in_bounds():
                        self.barrel_map.add(barrel)
                self.update_pixels()
                await self.shetty.turn(12)

    @logged
    async def goto_pos(self, waypoint, shorten=0):
        bearing, distance = self.shetty.get_azimuth_and_distance_to(waypoint)
        distance -= shorten
        if distance > 1000:  # if a long distance break into shorter sections
            print("breaking up long route")
            await self.goto_pos((waypoint - self.shetty.pos) / 2 + self.shetty.pos)
            await self.goto_pos(waypoint)
        else:
            with self.stabber.stab():
                await self.shetty.turn_to_azimuth(bearing)
            await self.eyeball.just_looking()
            await self.shetty.move(distance)
            await self.eyeball.just_looking()

    @logged
    async def follow_route(self, shorten=0):
        self.display.draw_text("Storing")
        for waypoint in self.route[1:]:
            if np.allclose(waypoint, self.route[-1]):
                shortening = shorten
            else:
                shortening = 0
            await self.goto_pos(waypoint, shortening)

    @logged
    async def retrieve_barrel(self, barrel):
        self.display.draw_text("Hunting")
        self.grabber.open()
        azimuth, _ = self.shetty.get_azimuth_and_distance_to(barrel.pos)
        with self.stabber.stab():
            await self.shetty.turn_to_azimuth(azimuth)
        await self.eyeball.just_looking()
        on_target, target = await self.fine_tune_grab(barrel)
        if not on_target:
            await self.shetty.move(-150)
            on_target, target = await self.fine_tune_grab(barrel)
            if not on_target:
                return False
        print(target, self.shetty.pos)
        distance = target.get_distance(self.shetty.pos)
        print("Distance to barrel: %d" % distance)
        if distance < 600:
            #distance = await self.get_distance()  # get accurate laser distance
            await self.shetty.move(distance - 50, speed=400)
        else:
            await self.shetty.move(distance - 300)
            expected_distance = 100
            count = 0
            while True:
                on_target, target = await self.fine_tune_grab(barrel)
                if on_target:
                    distance = target.get_distance(self.shetty.pos)
                    if distance < barrel.get_distance(self.shetty.pos) + expected_distance:  # looking good
                        break
                    else:
                        print("bad distance: ", distance, expected_distance)
                # something has gone wrong. Back off a bit and try again
                await self.shetty.move(-100)
                expected_distance += 100
                count += 1
                if count > 5:
                    # can't find it - has it rolled away?
                    self.barrel_map.remove(barrel)
                    return False
            await self.shetty.move(distance - 50, speed=400)
        self.grabber.close()
        self.barrel_map.remove(barrel)
        return True

    def draw(self, arena):
        self.shetty.draw(arena)
        self.barrel_map.draw(arena)
        if len(self.route) > 1:
            scaled_route = np.array(self.route) * arena.SCALE
            scaled_route[:, 1] = arena.screen.get_height() - scaled_route[:, 1]
            pygame.draw.lines(arena.screen, (255, 255, 0), False, scaled_route)

    async def process_barrel(self, barrel):
        if not await self.retrieve_barrel(barrel):
            return False
        if barrel.colour == "green":
            destination = (700, 2100)
            #destination = (450 + self.green_count * 100, 2100)
            self.green_count += 1
        else:
            destination = (1500, 2100)
            #destination = (1750 - self.red_count * 100, 2100)
            self.red_count += 1
        self.route = await self.barrel_map.calculate_route(self.shetty.pos, destination)
        await self.follow_route(shorten=50)
        self.grabber.release()
        self.update_pixels()
        await asyncio.sleep(0.5)
        await self.shetty.move(-250)
        return True

    async def run(self):
        self.stabber.release()
        await self.shetty.move(-100.0)
        self.grabber.release()

        # do first map and find first barrel
        await self.create_map(270, 90)
        self.eyeball.track_barrels = True
        target = self.barrel_map.get_nearest(self.shetty.pos)
        print(target)
        print(self.barrel_map)
        await self.process_barrel(target)

        # scan barrels from other direction
        i = 0

        while True:
            # if we think we've finished, or we've got four barrels
            if self.barrel_map.empty() or i % 4 == 0:
                await self.create_map(90, 270)
                if self.barrel_map.empty():
                    break
            target = self.barrel_map.get_nearest(self.shetty.pos)
            if not await self.process_barrel(target):
                self.barrel_map.clear()
                await self.create_map(90, 270)
            i += 1
        self.route = [self.shetty.pos, [1100, 1000]]
        await self.follow_route(shorten=0)
        await self.drive.dance()


class Test(EcoDisaster):

    async def run(self):
        await self.create_map(270, 90, thorough=True)
        target = self.barrel_map.get_nearest(self.shetty.pos)
        colour = await self.retrieve_barrel(target)
        print("Got a %s barrel" % colour)
        self.grabber.off()
