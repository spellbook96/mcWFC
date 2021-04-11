from worldLoader import WorldSlice
from nbt import *
import interfaceUtils


def writeData(worldslice, sPos, ePos, filename="sample.txt"):
    ws = worldslice
    s = sPos
    e = ePos
    fn = filename

    print("Writing building data: " + fn)
    print("Start postion =" +str(s)+ "End postion =" +str(e))
    cnt = 0
    with open(fn, 'w') as f:
        for x in range(s[0], e[0]+1):
            for y in range(s[1], e[1]+1):
                for z in range(s[2], e[2]+1):
                    block = ws.getBlockAt([x, y, z])
                    try:
                        name = str(block["Name"])
                    except:
                        #print(str(x-s[0])+" "+str(y-s[1])+" "+str(z-s[2]))
                        # print("error: can not write (%s,%s,%s) block" %
                        #       (x, y, z))
                        cnt += 1
                        continue
                    f.write(str(x-s[0])+" "+str(y-s[1])+" "+str(z-s[2]) + " ")
                    f.write(name)

                    try:
                        tmp = block["Properties"]
                        f.write(" [")
                        for tag in block["Properties"]:
                            f.write(tag+"="+str(block["Properties"][tag]))
                        f.write("]")
                    except:
                        pass

                    f.write("\n")
    print(str(cnt)+" error")
    print("complete")


class buildingData:
    def __init__(self,level, filename=""):
        self.fn = filename
        f = open(self.fn)
        self.blocks = f.read().splitlines()
        self.st = []
        self.level = level

    def build(self, x, y, z):
        
        print("building " + self.fn)

        self.st = [x, y, z]
        for block in self.blocks:
            data = block.split(" ")
            _x = int(data[0])
            _y = int(data[1])
            _z = int(data[2])
            self.level.setBlock(_x+x, _y+y, _z+z, data[3])
            #print("setBlock(%s,%s,%s,%s)" % (_x+x,_y+y,_z+z,data[3]))

        self.level.flush()

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
        self.flush()
        self.level.redo_flag=True
