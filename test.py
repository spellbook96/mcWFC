from Level import *
import random
from Cityscape import *
from buildingData import *

level = Level(USE_BATCHING=2000,hm=False)
area = level.getBuildArea()
x_start = area[0]
z_start = area[1]
x_size = area[2]
z_size = area[3]
x_end = x_start + x_size
z_end = z_start + z_size
x_center = int((x_start + x_end) /2)
z_center = int((z_start + z_end) /2)
import time
x,z = 999,999
bd = buildingData(level,filename="house_5x5_wood.txt")
while(1):
    f = open('position.txt', 'r')
    data=f.read()
    if (data==""):
        time.sleep(1)
        continue
    if(data=="q"):
        break
    _x,_z= data.rsplit(" ")
    _x=int(_x);_z=int(_z)
    if(_x!=x or _z!=z):
        x=int(_x);z=int(_z)
        print(x,z)
        bd.build(x_center+x*10,4,z_center+z*10)
    time.sleep(1)

level.undo()