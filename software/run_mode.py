#!/usr/bin/env python3
import asyncio
import sys

from modes import shooter, escape, manual, eco, lava
import calibrate
from main import Main
import logging
import argparse
logging.basicConfig(filename='run_mode.log',level=logging.INFO)


async def go(main, main_task, mode):
    await asyncio.sleep(1)
    await m.enter_mode(mode)
    m.exit()
    await main_task
    print("Main has finished")
    
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Mode to run", nargs='?', default="escape.Learn")
parser.add_argument("-s", "--simulation", help="Run in a simulation", nargs='?', const="simulation.Arena")
args = parser.parse_args()

mode = eval(args.mode)
print(args)
loop = asyncio.get_event_loop()
loop.set_debug(False)



if args.simulation:
    import simulation
    arena = eval(args.simulation)()
    simulation.Hardware.set_arena(arena)
    pygame_task = loop.create_task(arena.pygame_loop())
    hardware = simulation
else:
    hardware = None

m = Main(hardware)
main_task = loop.create_task(m.run())

if args.simulation:
    arena.add_object(m)

try:
    loop.run_until_complete(go(m, main_task, mode))
finally:
    m.hardware.drive.stop()
    
