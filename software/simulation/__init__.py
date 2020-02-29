"""Hardware representations for Shetland Attack Pony: mobile"""
from .arena import Arena
from .camera import Camera
from .controller import Controller
from .display import Display
from .drivetrain import Drive
from .ecoarena import EcoArena
from .encoder import Encoder
from .grabber import Grabber
from .laser import Laser
from .lava import LavaArena
from .minefield import MineField
from .pixels import Pixels
from .shetty import Shetty


class Hardware:
    def __init__(self, queue):
        self.drive = Drive(self.shetty)
        self.encoder = Encoder(queue)
        self.controller = Controller(queue)
        self.pixels = Pixels()
        self.laser = Laser(self.shetty, self.arena)
        self.camera = Camera(self.arena)
        self.display = Display()
        self.shooter = None
        self.grabber = Grabber(self.shetty, self.arena)
        self.stabber = None

    @classmethod
    def set_arena(cls, arena):
        cls.arena = arena
        cls.shetty = arena.get_shetty()
