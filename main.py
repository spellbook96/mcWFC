from Level import *
level = Level(USE_BATCHING=2000)

area = level.getBuildArea()
x_start = area[0]
z_start = area[1]
x_size = area[2]
z_size = area[3]
x_end = x_start + x_size
z_end = z_start + z_size
x_center = int((x_start + x_end) /2)
z_center = int((z_start + z_end) /2)

level.calculate_Quadtree(mgw =10,mfw=2,qms = 40,qi=5)
qm = level.getQuadtree()
level.plotMap()
for z in range(z_size):
    for x in range(x_size):
        # if bm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==0:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        if qm[x,z]==1:
            level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"smooth_red_sandstone_slab")
level.flush()

QL = level.getQuadtreeList()
from Prototypes import Prototypes
from wfc import *
prototypes = Prototypes(level=level)
bd =prototypes.read("prototypes_27.txt")
wfc = WFC(10,15,10,bd,AUTO=0)
r=False
while r==False:
    r = wfc.run(level=level,visualize=False)
    print(r)

for p in QL:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    size=(p[1][0],p[1][1])
    if(size[0]>=40 and size[1]>=40):
        wfc.setBuilding(x,y,z)

#--------------------
level.calculate_Quadtree(mgw =1,mfw=1,qms = 10,qi=1)
qm = level.getQuadtree()
level.plotMap()

for z in range(z_size):
    for x in range(x_size):
        # if bm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==0:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        if qm[x,z]==1:
            level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"smooth_red_sandstone_slab")

level.flush()

QL = level.getQuadtreeList()
from buildingData import *
b_small = buildingData(level,"house.txt")
b_sand = buildingData(level,"small.txt")
b_7x7 = buildingData(level,"7x7cube.txt")
# b.build(x_center,level.getHeightAt(x_center,z_center),z_center)
for p in QL:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    size=(p[1][0],p[1][1])
    if(size[0]==7 and size[1]==7):
        b_7x7.build(x,y,z)
    elif (size[0] <7 or size[1] <7) and size[0] > 5 and size[1]>5:
        b_sand.build(x,y,z)
    
    elif p[1][0] >10 and p[1][1] >10:
        b_small.build(x,y,z)
level.flush()




import time

time.sleep(60)
print("undo")
level.undo()