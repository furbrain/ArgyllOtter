import cv2
import numpy as np

from compute import vision
from modes import mode
from util import spawn

DRIVE_SPEED = 400
TURN_SPEED = DRIVE_SPEED * 0.7


class Lava(mode.Mode):
    HARDWARE = ('drive', 'camera')
    TURNS = "l"

    async def find_lines(self, debug=False):
        img = self.camera.get_image(fast=True)
        if debug:
            cv2.imwrite("original.png", img)
        cropped = img[240:, :]
        lines = await spawn(vision.find_lines, cropped, debug)
        if debug:
            for x1, y1, x2, y2, angle, rho in lines:
                cv2.line(img, (int(x1), int(y1 + 240)), (int(x2), int(y2 + 240)), (0, 255, 0), 2)
            cv2.imwrite("lined.png", img)
        return lines

    def veer_left(self):
        print("<")
        self.drive.drive(TURN_SPEED, DRIVE_SPEED)

    def veer_right(self):
        print(">")
        self.drive.drive(DRIVE_SPEED, TURN_SPEED)

    def go_straight(self):
        print("|")
        self.drive.drive(DRIVE_SPEED)

    @staticmethod
    def get_current_line(lines):
        matches = []
        for x1, y1, x2, y2, angle, rho in lines:
            if -40 < angle < 40:
                if y1 > 140:
                    matches.append([angle, x1, y2])
                elif y2 > 140:
                    matches.append([angle, x2, y1])
        if len(matches) == 0:
            return None, None, None
        elif len(matches) == 1:
            return matches[0]
        elif len(matches) == 2:
            return np.mean(matches, axis=0)
        else:
            left = np.array(min(matches))
            right = np.array(max(matches))
            return (left + right) / 2

    @staticmethod
    def line_ends_at_centre(lines):
        x1, y1, x2, y2, angle, rho = lines.T
        end1 = (240 < x1) & (x1 < 400) & (y1 > 180)
        end2 = (240 < x2) & (x2 < 400) & (y2 > 180)
        return end1 | end2

    def get_next_line(self, lines, direction):
        matches = []
        if len(lines) == 0:
            return None, None
        x1, y1, x2, y2, angle, rho = lines.T
        if direction == "r":
            matches = np.logical_and(-80 < angle, angle < -20)
        else:
            matches = np.logical_and(20 < angle, angle < 80)
        matches = np.logical_and(matches, self.line_ends_at_centre(lines))
        if not any(matches):
            return None, None
        matches = lines[matches]
        x1, y1, x2, y2, angle, rho = matches.T
        if direction == "r":
            startx = np.minimum(x1, x2)
            endx = np.maximum(x1, x2)
        else:
            startx = np.maximum(x1, x2)
            endx = np.minimum(x1, x2)
        starty = np.maximum(y1, y2)
        endy = np.minimum(y1, y2)
        start = self.camera.get_position(np.mean(startx), np.mean(starty) + 240)
        end = self.camera.get_position(np.mean(endx), np.mean(endy) + 240)
        vector = end - start
        angle = np.arctan2(vector[1], vector[0])
        return np.rad2deg(angle), start[1]

    async def follow_line(self, direction, debug=False):
        last_distance = 180
        while True:
            lines = await self.find_lines(debug)
            if lines is not None:
                angle, pos, distance = self.get_current_line(lines)
                if angle is None:
                    print("Lines:", lines)
                    angle, _ = self.get_next_line(lines, direction)
                    return angle, last_distance
            else:
                print("Lines:", lines)
                return 0, last_distance
            last_distance = self.camera.calibration.get_distance(distance)
            print(last_distance)
            if 240 < pos < 400:
                if angle < -10:
                    self.veer_left()
                elif angle > 10:
                    self.veer_right()
                else:
                    self.go_straight()
            elif pos < 240:
                self.veer_left()
            elif pos > 400:
                self.veer_right()

    async def run(self):
        self.go_straight()
        while True:
            lines = await self.find_lines()
            current, _, _ = self.get_current_line(lines)
            if current is not None:
                break
        for direction in self.TURNS:
            angle, distance = await self.follow_line(direction)
            print("distance", distance)
            # if distance is not None:
            #    await self.drive.a_goto(DRIVE_SPEED, distance, fast=True)
            # else:
            #    print("guessing")
            #    await self.drive.a_goto(DRIVE_SPEED, 100, fast=True)
            if direction == "r":
                await self.drive.fast_turn(45, TURN_SPEED, differential=0)
            else:
                await self.drive.fast_turn(-45, TURN_SPEED, differential=0)
            while True:
                break
                lines = await self.find_lines()
                current, _, _ = self.get_current_line(lines)
                if current is not None:
                    break
            self.go_straight()
        await self.follow_line("r", debug=True)
        # await self.drive.a_goto(DRIVE_SPEED,700)
        self.drive.stop()
