#!/usr/bin/env python3
import asyncio
import sys

from modes import shooter, escape
from main import Main
import logging
logging.basicConfig(filename='run_mode.log',level=logging.DEBUG)


async def go(loop, mode):
    m = Main()
    main_task = loop.create_task(m.run())
    await asyncio.sleep(1)
    m.enter_mode(mode)
    await main_task
    print("Main has finished")
    
default = escape.Learn
if len(sys.argv) > 1:
    mode = eval(sys.argv[1])
else:
    mode = default
loop = asyncio.get_event_loop()
loop.set_debug(False)
loop.run_until_complete(go(loop, mode))
