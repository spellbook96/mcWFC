from worldLoader import WorldSlice
from nbt import *
import interfaceUtils
import numpy as np

def writeData(level, sPos, ePos, filename="sample.txt"):
    s = sPos
    e = ePos
    fn = filename

    print("-------------------------------------------")
    print("Writing building data: " + fn)
    print("Start postion =" +str(s)+ " End postion =" +str(e))
    cnt = 0
    bcnt =0
    space =100
    with open(fn, 'w') as f:
        x_size = e[0]-s[0]+1
        y_size = e[1]-s[1]+1
        z_size = e[2]-s[2]+1
        f.write("%s %s %s\n" % (x_size,y_size,z_size))
        for y in range(e[1],s[1]-1,-1):
            for z in range(s[2], e[2]+1):
                for x in range(s[0], e[0]+1):
                    block = level.getBlockCompoundAt(x, y, z)
                    if block == None:
                        f.write("air[]")
                        for n in range(space-5):
                            f.write(" ")
                        bcnt+=1
                        continue
                    try:
                        name = str(block["Name"])
                    except:
                        print("error: can not write (%s,%s,%s) block" %
                              (x, y, z))
                        cnt += 1
                        continue

                    cell=name

                    try:
                        tmp = block["Properties"]
                        cell+="["
                        for tag in block["Properties"]:
                            cell= cell+tag+"="+str(block["Properties"][tag])+","
                        cell+="]"
                        bcnt +=1
                    except:
                        cell+="[]"

                    for n in range(space-len(cell)):
                        cell +=" "
                    
                    cell = cell.replace("minecraft:","")
                    f.write(cell)
                f.write("\n")
            f.write("\n")
    #print(str(cnt)+" error")
    print("total %d blocks" % bcnt)


class buildingData:
    def __init__(self,level, filename=""):
        if filename == "":
            pass
        else:
            self.fn = filename
            f = open(self.fn)
            self.blocks = f.read().splitlines()
        self.st = []
        self.level = level

    def build(self, x, y, z):
        print("-------------------------------------------")
        # print("building " + self.fn)
        print("building " + self.fn +" at (%d %d %d)" %(x,y,z))
        from time import time
        begin_time = time()
        self.st = [x, y, z]
        for block in self.blocks:
            data = block.split(" ")
            _x = int(data[0])
            _y = int(data[1])
            _z = int(data[2])
            # self.level.setBlock(_x+x, _y+y, _z+z, data[3])
            self.level.setBlock(_x+x, _y+y, _z+z, data[3])
            #print("setBlock(%s,%s,%s,%s)" % (_x+x,_y+y,_z+z,data[3]))

        self.level.flush()

        # Calculate run time
        end_time = time()
        run_time = end_time - begin_time
        print ("runtime: %.2f s" % run_time)

    def catch(self,sPos, ePos,filename="temp"):
        writeData(self.level,sPos,ePos,filename=filename)
        self.__init__(self.level,filename=filename)


    def clear(self, x=0, y=0, z=0):
        self.level.undo_flag=False
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
        self.level.undo_flag=True

    def getBuildingData(self):
        size_x =0
        size_y =0
        size_z= 0
        for block in self.blocks:
            data = block.split(" ")
            size_x = int(data[0])
            size_y = int(data[1])
            size_z = int(data[2])

        blockList= [[[0 for _ in range(size_x+1)] for _ in range(size_z+1)] for _ in range(size_y+1)] #Block ID list shape[y][z][x]
        IDtoName ={}
        NametoID ={}
        index = -1
        PList = []
        for block in self.blocks:
            data = block.split(" ")
            _x = int(data[0])
            _y = int(data[1])
            _z = int(data[2])
            if data[3] not in NametoID :
                index +=1
                IDtoName[index] = data[3]
                NametoID[data[3]] = index
                PList.append(index)

            blockList[_y][_z][_x]= NametoID[data[3]]

        # print("%d %d %d" % (size_x,size_z,size_y))
        # blockArr = np.array(blockList)
        # y,z,x = blockArr.shape
        return blockList,PList,IDtoName,NametoID


if __name__ == "__main__":
    from Level import *
    level = Level(USE_BATCHING=1000,hm=False)

    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size
    x_center = int((x_start + x_end) /2)
    z_center = int((z_start + z_end) /2)


# write building //b.catch(startpos,endpos,filename)

    # print(x_start)
    b = buildingData(level)
    b.catch((-233, 4, 19),(-219, 8, 33),"wfc_15x15_1.txt")
    # b.build(26,4,22)  //test

# build // buildingData(level,filename)   b.build(x,y,z)

    # b = buildingData(level,"fence_base.txt")
    # b.build(x_center,level.getHeightAt(x_center,z_center),z_center)

    # import time

    # time.sleep(10)
    # print("undo")
    # level.undo()

# test

    # b = buildingData(level,"house.txt")
    # b.build(x_center,level.getHeightAt(x_center,z_center),z_center)
    # import time
    # time.sleep(10)
    # print("undo")
    # level.undo()
