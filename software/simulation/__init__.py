"""Hardware representations for Shetland Attack Pony: mobile"""
from .drivetrain import Drive
from .encoder import Encoder
from .laser import Laser
from .display import Display
from .controller import Controller
from .pixels import Pixels
from .camera import Camera
from .shetty import Shetty
from .arena import Arena
from .grabber import Grabber
from .ecoarena import EcoArena
from .lava import LavaArena



class Hardware:
    def __init__(self, queue):
        self.drive = Drive(self.shetty)
        self.encoder = Encoder(queue)
        self.controller = Controller(queue)
        self.pixels = Pixels()
        self.laser = Laser(self.shetty, self.arena)
        self.camera = Camera(self.arena)
        self.display = None
        self.shooter = None
        self.grabber = Grabber()
        
    @classmethod
    def set_arena(cls, arena):
        cls.arena = arena
        cls.shetty = arena.get_shetty()
    
