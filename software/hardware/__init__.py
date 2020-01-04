"""Hardware representations for Shetland Attack Pony: mobile"""
from .drivetrain import Drive
from .grabber import Grabber
from .shooter import Shooter
from .encoder import Encoder
from .laser import Laser
from .display import Display
from .controller import Controller
from .pixels import Pixels
from .camera import Camera

class Hardware:
    def __init__(self, queue):
        self.drive = Drive()
        self.encoder = Encoder(queue)
        self.controller = Controller(queue)
        self.pixels = Pixels()
        self.laser = Laser()
        
        try:
            self.camera = Camera()
        except IOError:
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
