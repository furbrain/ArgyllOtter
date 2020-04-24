# Shetland Attack Pony: Mobile

This is the code, construction files, pcb designs and firmware for the Shetland Attack Pony: Mobile, an 
entry to [Pi Wars 2020](https://piwars.org/).

## Why the silly name?
For the last 10 years, I have been developing a cave surveying tool called the [Shetland Attack Pony](https://github.com/furbrain/SAP5/). This uses a laser range finder, an OLED screen and a 9 axis magnetometer, accelerometer and gyro, and a PIC controller. The robot uses all of these components plus some motors and a raspberry pi, so it seemed a fitting name.

## What parts did you use?
Most of the chassis we have made ourselves with laser-cut acrylic and 3d printed parts. We have made our own pcbs with a CNC engraver/miller. 

Other components used:
* Raspberry Pi 3A
* 2200 mAh LiPo Battery (11.1V)
* [FIT0493](https://www.dfrobot.com/product-1462.html) 12V motor with encoder
* [TLE52602 motor driver](https://uk.rs-online.com/web/p/motor-driver-ics/9062978/) (x4)
* [PIC16F18877](https://www.microchip.com/wwwproducts/en/PIC16F18877) as a motor sub-controller - this allows the PI to
send a command over I2C saying "Drive forward 1m, then stop", this makes some of the autonomous challenges much easier
* [MPU9250](https://shop.pimoroni.com/products/sparkfun-imu-breakout-mpu-9250) 9 axis magnetometer, gyro and accelerometer
* [Laser range finder from aliexpress](https://www.aliexpress.com/item/4000429728611.html)

For the autonomous challenges:
* A caving helmet and light!
* A Raspberry Pi Zero Camera

For the Zombie Apocalypse Challenge:
* [Atomic power popper](https://www.amazon.co.uk/ATOMIC-POWER-POPPER-Battle-Foams/dp/B07GV3S912) - Cut this down to 
make the barrel of the cannon
* [BMP388](https://shop.pimoroni.com/products/adafruit-bmp388-precision-barometric-pressure-and-altimeter) Pressure sensor
* Another MPU9250 to measure inclination
* 12V air pump to pressurise the barrel.

## What software did you use?

We used [Freecad](https://www.freecadweb.org/) to design all the laser-cut and 3d printed parts, and  we used [gEDA](http://www.geda-project.org/) for all the PCB design.

We also used the following python libraries:
* [OpenCV](https://opencv.org/) for computer vision
* [shapely](https://pypi.org/project/Shapely/) and [pyvisgraph](https://github.com/TaipanRex/pyvisgraph) to work out an efficient route through barrels for Eco-Disaster

For the simulation code we used [pygame](http://pygame.org) for the top downview and [vtk](https://pypi.org/project/vtk/) for the 3d view
