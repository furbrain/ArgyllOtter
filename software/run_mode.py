#!/usr/bin/env python3
import argparse
import asyncio
import logging

# noinspection PyUnresolvedReferences
import calibrate
# noinspection PyUnresolvedReferences
import modes
from main import Main

logging.basicConfig(filename='run_mode.log', level=logging.INFO)


async def go(m, task, mode, pg_task):
    await asyncio.sleep(0.1)
    if pg_task:
        done, pending = await asyncio.wait((m.enter_mode(mode), pg_task), return_when=asyncio.FIRST_COMPLETED)
        for d in done:
            d.result()
    else:
        await m.enter_mode(mode)
    m.exit()
    await task
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

main = Main(hardware)
main_task = loop.create_task(main.run())

if args.simulation:
    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
    arena.add_object(main)

try:
    loop.run_until_complete(go(main, main_task, run_mode, pygame_task))
finally:
    main.hardware.drive.stop()
