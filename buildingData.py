from worldLoader import WorldSlice
from nbt import *
import interfaceUtils
import time


def writeData(level, sPos, ePos, filename="sample.txt"):
    s = sPos
    e = ePos
    fn = filename

    print("-------------------------------------------")
    print("Writing building data: " + fn)
    print("Start postion =" +str(s)+ " End postion =" +str(e))
    cnt = 0
    bcnt =0
    with open(fn, 'w') as f:
        for x in range(s[0], e[0]+1):
            for y in range(s[1], e[1]+1):
                for z in range(s[2], e[2]+1):
                    block = level.getBlockCompoundAt(x, y, z)
                    if block == None:
                        f.write(str(x-s[0])+" "+str(y-s[1])+" "+str(z-s[2]) + " ")
                        f.write("minecraft:air\n")
                        bcnt+=1
                        continue
                    try:
                        name = str(block["Name"])
                    except:
                        print(str(x-s[0])+" "+str(y-s[1])+" "+str(z-s[2]))
                        print("error: can not write (%s,%s,%s) block" %
                              (x, y, z))
                        cnt += 1
                        continue

                    f.write(str(x-s[0])+" "+str(y-s[1])+" "+str(z-s[2])+ " ")
                    f.write(name)

                    try:
                        tmp = block["Properties"]
                        f.write("[")
                        for tag in block["Properties"]:
                            f.write(tag+"="+str(block["Properties"][tag])+",")
                        f.write("]")
                        bcnt +=1
                    except:
                        pass

                    f.write("\n")
    #print(str(cnt)+" error")
    print("total %d blocks" % bcnt)


class buildingData:
    def __init__(self,level, filename=""):
        self.fn = filename
        f = open(self.fn)
        self.blocks = f.read().splitlines()
        self.st = []
        self.level = level

    def build(self, x, y, z):
        print("-------------------------------------------")
        # print("building " + self.fn)
        print("building " + self.fn +" at (%d %d %d)" %(x,y,z))
        # begin_time = time()
        self.st = [x, y, z]
        for block in self.blocks:
            data = block.split(" ")
            _x = int(data[0])
            _y = int(data[1])
            _z = int(data[2])
            self.level.setBlock(_x+x, _y+y, _z+z, data[3])
            #print("setBlock(%s,%s,%s,%s)" % (_x+x,_y+y,_z+z,data[3]))

        self.level.flush()

        # # Calculate run time
        # end_time = time()
        # run_time = end_time - begin_time
        # print ("runtime: %.2f s" % run_time)

    def clear(self, x=0, y=0, z=0):
        self.level.redo_flag=False
        if(x == 0 and y == 0 and z == 0):
            x = self.st[0]
            y = self.st[1]
            z = self.st[2]
        for block in self.blocks:
            data = block.split(" ")
            _x = int(data[0])
            _y = int(data[1])
            _z = int(data[2])
            self.level.setBlock(_x+x, _y+y, _z+z, "air")
        self.level.flush()
        self.level.redo_flag=True

if __name__ == "__main__":
    from Level import *
    level = Level(USE_BATCHING=50)

    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size
    x_center = int((x_start + x_end) /2)
    z_center = int((z_start + z_end) /2)

    writeData(level, (172,4,-3), (182,10,5), filename="house.txt")