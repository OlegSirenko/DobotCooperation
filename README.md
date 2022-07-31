# DobotCooperation
Two Dobots cooperation. Used Dobot studio and PyDobot

## Realisation video: https://www.youtube.com/watch?v=biJJbaEPKKs

## How does it works?
- First you need to install [Dobot Studio](https://www.dobot.cc/downloadcenter/dobot-magician.html)
- Next to install [PyDobot](https://pypi.org/project/pydobot2/)

Please note that Padobot does not have access to sensors, thats why we use two scripts.

First script - [NewGrippingCubeFromRail](../main/NewGrippingCubeFromRail.py). This script for IDE Dobot Studio.
Second script - [main_function](../main/main_function.py). This script for Python IDE.

## If you don't need sensors in your project
Just use pyDobot. There is example of code:
```python
from pydobot import Dobot

dobot1 = Dobot(port="COM4")  # init DOBOT (always check COM port)
dobot2 = Dobot(port="COM5")  # init DOBOT (always check COM port)

x, y, z, r = dobot1.get_pose().position  # getting pose of dobot, to have x, y, z
dobot1.move_to(x, y, z - 15)

x, y, z, r = dobot2.get_pose().position  # getting pose of dobot, to have x, y, z
dobot2.move_to(x, y, z - 15)

dobot1.conveyor_belt_distance(speed=26.5, distance=10000, direction=1) # use 1 if you need to forward conveyor belt to wires of connection 
```

