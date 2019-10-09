v 20130925 2
C 43400 45700 1 0 0 raspberry_pi_2.sym
{
T 47000 52500 5 10 1 1 0 6 1
refdes=PI
T 43700 49900 5 10 0 0 0 0 1
device=RaspberryPi2
T 43395 46200 5 10 0 1 0 0 1
footprint=HEADER40_2
}
C 40900 49700 1 0 0 3.3V-plus-1.sym
C 47900 52500 1 0 0 5V-plus-1.sym
C 42600 48200 1 0 0 gnd-1.sym
N 48100 52500 48100 52100 4
N 48100 52100 47500 52100 4
N 47500 52100 47500 51800 4
N 47500 51500 48800 51500 4
C 43400 51900 1 180 0 io-1.sym
{
T 42500 51700 5 10 0 0 180 0 1
net=SDA:1
T 43200 51300 5 10 0 0 180 0 1
device=none
T 42500 51800 5 10 1 1 180 1 1
value=SDA
}
C 43400 51600 1 180 0 io-1.sym
{
T 42500 51400 5 10 0 0 180 0 1
net=SCL:1
T 43200 51000 5 10 0 0 180 0 1
device=none
T 42500 51500 5 10 1 1 180 1 1
value=SCL
}
C 43400 51300 1 180 0 io-1.sym
{
T 42500 51100 5 10 0 0 180 0 1
net=ALERT:1
T 43200 50700 5 10 0 0 180 0 1
device=none
T 42500 51200 5 10 1 1 180 1 1
value=ALERT
}
C 47500 51100 1 0 0 io-1.sym
{
T 48400 51300 5 10 0 0 0 0 1
net=TX:1
T 47700 51700 5 10 0 0 0 0 1
device=none
T 48400 51200 5 10 1 1 0 1 1
value=Tx
}
C 47500 50800 1 0 0 io-1.sym
{
T 48400 51000 5 10 0 0 0 0 1
net=RX:1
T 47700 51400 5 10 0 0 0 0 1
device=none
T 48400 50900 5 10 1 1 0 1 1
value=RX
}
C 43400 47400 1 180 0 io-1.sym
{
T 42500 47200 5 10 0 0 180 0 1
net=NEOPIXEL:1
T 43200 46800 5 10 0 0 180 0 1
device=none
T 42500 47300 5 10 1 1 180 1 1
value=NEOPIXEL
}
N 43400 48500 42700 48500 4
C 48700 51200 1 0 0 gnd-1.sym
C 43400 46800 1 180 0 io-1.sym
{
T 42500 46600 5 10 0 0 180 0 1
net=DT:1
T 43200 46200 5 10 0 0 180 0 1
device=none
T 42500 46700 5 10 1 1 180 1 1
value=DT
}
C 43400 47100 1 180 0 io-1.sym
{
T 42500 46900 5 10 0 0 180 0 1
net=SW:1
T 43200 46500 5 10 0 0 180 0 1
device=none
T 42500 47000 5 10 1 1 180 1 1
value=SW
}
N 43400 49700 41100 49700 4
C 43400 50400 1 180 0 io-1.sym
{
T 42500 50200 5 10 0 0 180 0 1
net=PUMP:1
T 43200 49800 5 10 0 0 180 0 1
device=none
T 42500 50300 5 10 1 1 180 1 1
value=PUMP
}
C 43400 50500 1 0 1 io-1.sym
{
T 42500 50700 5 10 0 0 0 6 1
net=SERVO:1
T 43200 51100 5 10 0 0 0 6 1
device=none
T 42500 50600 5 10 1 1 0 7 1
value=SERVO
}
C 43400 50100 1 180 0 io-1.sym
{
T 42500 49900 5 10 0 0 180 0 1
net=POINTER:1
T 43200 49500 5 10 0 0 180 0 1
device=none
T 42500 50000 5 10 1 1 180 1 1
value=POINTER
}
C 43400 47700 1 180 0 io-1.sym
{
T 42500 47500 5 10 0 0 180 0 1
net=CLK:1
T 43200 47100 5 10 0 0 180 0 1
device=none
T 42500 47600 5 10 1 1 180 1 1
value=CLK
}
