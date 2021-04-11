from nbt import *
import csv
import numpy as np
import interfaceUtils


class nbt_reader:
    def __init__(self):
        self.pal = []
        self.pos = []

    def load(self, filename=None):
        self.fn = filename
        self.nbtfile = nbt.NBTFile(self.fn, "rb")
        pos = []
        state = []

        for tag in self.nbtfile["blocks"].tags:
            pos.append([str(tag["pos"][0]), str(
                tag["pos"][1]), str(tag["pos"][2])])
            state.append(str(tag["state"]))

        palette_dict = {}
        palette_list = list()
        i = 0
        for tag in self.nbtfile['palette'].tags:
            tmp = str(tag['Name'])
            try:
                var = str(tag["Properties"]["variant"])
                print("found var: " +var)
                print(tmp)
                tmp = tmp.replace("minecraft:", "")
                if var not in tmp:
                    tmp = "minecraft:"+var + "_"+tmp
                
                print(tmp)
                palette_dict[i] = tmp
                palette_list.append(tmp)
            except:
                palette_dict[i] = tmp
                palette_list.append(tmp)

            i += 1

        palette = []

        for j in range(len(state)):
            palette.append(palette_dict[int(state[j])])

        self.pal = palette
        self.pos = pos

    def build(self, x, y, z):
        self.sx = x
        self.sy = y
        self.sz = z
        i = 0
        for place in self.pos:
            x, y, z = place
            x = int(x)
            y = int(y)
            z = int(z)
            x += self.sx
            z += self.sz
            y += self.sy
            # print(x,y,z)
            self.setBlock(x, y, z, self.pal[i])
            i += 1
        self.flush()

    def setBlock(self, x, y, z, block):
        interfaceUtils.placeBlockBatched(x, y, z, block, 100)

    def flush(self, batch=100):
        for i in range(100):
            self.setBlock(0, 100, 0, "air")

    def clear(self):
        i = 0
        for place in self.pos:
            x, y, z = place
            x = int(x)
            y = int(y)
            z = int(z)
            x += self.sx
            z += self.sz
            y += self.sy
            # print(x,y,z)
            self.setBlock(x, y, z, "air")
            i += 1
        self.flush()

    def print(self):
        with open("nbt_printout.txt","w") as f:
            f.write(self.nbtfile.pretty_tree())
