#!/usr/bin/env python3
from modes import shooter
from main import Main
import asyncio

print("started")
async def go(loop):
    m = Main()
    print("going...")
    main_task = loop.create_task(m.run())
    await asyncio.sleep(1)
    m.enter_mode(shooter.Shooter)
    await main_task
    print("Main has finished")
    
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(go(loop))
