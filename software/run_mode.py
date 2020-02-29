#!/usr/bin/env python3
import asyncio
import sys

from modes import shooter, escape, manual, eco, lava, mode, minesweeper
import calibrate
from main import Main
import logging
import argparse
logging.basicConfig(filename='run_mode.log',level=logging.INFO)


async def go(main, main_task, mode, pygame_task):
    await asyncio.sleep(0.1)
    if pygame_task:
        done, pending  = await asyncio.wait((m.enter_mode(mode),pygame_task), return_when=asyncio.FIRST_COMPLETED)
        for d in done:
            d.result()
    else:
        await m.enter_mode(mode)
    m.exit()
    await main_task
    print("Main has finished")
    
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Mode to run", nargs='?', default="escape.Learn")
parser.add_argument("-s", "--simulation", help="Run in a simulation", nargs='?', const="simulation.Arena")
args = parser.parse_args()

run_mode = eval(args.mode)
print(args)
loop = asyncio.get_event_loop()
loop.set_debug(True)



if args.simulation:
    import simulation
    arena = eval(args.simulation)()
    simulation.Hardware.set_arena(arena)
    pygame_task = loop.create_task(arena.pygame_loop())
    hardware = simulation
else:
    hardware = None
    pygame_task = None

m = Main(hardware)
main_task = loop.create_task(m.run())

if args.simulation:
    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
    arena.add_object(m)

try:
    loop.run_until_complete(go(m, main_task, run_mode, pygame_task))
finally:
    m.hardware.drive.stop()
    
