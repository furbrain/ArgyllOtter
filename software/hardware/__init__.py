"""Hardware representations for Shetland Attack Pony: mobile"""
import picamera

from .camera import Camera
from .controller import Controller
from .display import Display
from .drivetrain import Drive
from .encoder import Encoder
from .grabber import Grabber
from .laser import Laser, LaserTimeoutError, LaserBadReadingError
from .pixels import Pixels
from .shooter import Shooter
from .stabber import Stabber


class Hardware:
    def __init__(self, queue):
        self.drive = Drive()
        self.encoder = Encoder(queue)
        self.controller = Controller(queue)
        try:
            self.pixels = Pixels()
        except RuntimeError:
            self.pixels = None
            print("Unable to start neopixels - are you root?")
        self.laser = Laser()

        try:
            self.camera = Camera()
        except picamera.exc.PiCameraError:
            self.camera = None

        try:
            self.display = Display()
        except IOError:
            self.display = None

        try:
            self.shooter = Shooter()
        except IOError:
            self.shooter = None
        self.grabber = Grabber()
        self.stabber = Stabber()
