#!/usr/bin/env python3
import asyncio
import sys

from modes import shooter, escape
import calibrate
from main import Main
import logging
from hardware import Drive
logging.basicConfig(filename='run_mode.log',level=logging.INFO)


async def go(main, main_task, mode):
    await asyncio.sleep(1)
    await m.enter_mode(mode)
    m.exit()
    await main_task
    print("Main has finished")
    
default = escape.Learn
if len(sys.argv) > 1:
    mode = eval(sys.argv[1])
else:
    mode = default
loop = asyncio.get_event_loop()
loop.set_debug(False)
m = Main()
main_task = loop.create_task(m.run())
try:
    loop.run_until_complete(go(m, main_task, mode))
finally:
    m.driver.stop()
    
