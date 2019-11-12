#!/usr/bin/env python3
from hardware import Drive
import sys
import asyncio

d = Drive()

async def go(angle):
    await d.spin(angle, 200)

angle = float(sys.argv[1])
loop = asyncio.get_event_loop()
loop.run_until_complete(go(angle))
