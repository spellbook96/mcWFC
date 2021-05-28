import numpy as np
def makePrototypes(level,pos,N,PStep=1,length=1,fn="prototypes"):
    s = pos

    print("-------------------------------------------")
    print("Writing Prototypes: " + fn)
    print("Start postion =" +str(pos))
    print("N = " +str(N))
    print("Length =" +str(length))

    with open(fn, 'w') as f:
        f.write(str(N)+"\n")
        f.write(str(PStep)+"\n")
        f.write(str(length)+"\n")
        cnt = 0
        bcnt =0
        for i in range(length):
            if i>0:
                s = (s[0]+(N+1),s[1],s[2])
            e = (s[0]+N,s[1]+N,s[2]+N)
            for x in range(s[0], e[0]):
                for y in range(s[1], e[1]):
                    for z in range(s[2], e[2]):
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
                        if name == "minecraft:grass_block":
                            f.write("minecraft:dirt\n")
                            bcnt += 1
                            continue
                        else:
                            f.write(name)
                            bcnt +=1

                        try:
                            tmp = block["Properties"]
                            f.write("[")
                            for tag in block["Properties"]:
                                f.write(tag+"="+str(block["Properties"][tag])+",")
                            f.write("]")
                        except:
                            pass
                        f.write("\n")

    print("total %d blocks" % bcnt)



from buildingData import *
from Level import *
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
makePrototypes(level,pos=(26,4,22),N=5,PStep=4,length=27,fn="prototypes_27.txt")