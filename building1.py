from prototype import Prototype
from config import Config
import random


class Building:
    def __init__(self, sizeX, sizeZ, sizeY, config_file="config.json"):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.config = Config(config_file)
        self.Prototype_names = self.config.getKey("Prototypes")

        self.wave_fuction = []
        for _y in range(self.sizeY):
            y = []
            for _z in range(self.sizeZ):
                x = []
                for _x in range(self.sizeX):
                    if(_x == 0 or _x == sizeX-1 or _z == 0 or _z == sizeZ-1):
                        prototypes = []
                        tmp = Prototype("Empty", self.config)
                        tmp.setPos([_y, _z, _x])
                        prototypes.append(tmp)
                        x.append(prototypes)
                    else:
                        prototypes = []
                        for name in self.Prototype_names:
                            tmp = Prototype(name, self.config)  # dirct
                            tmp.setPos([_y, _z, _x])
                            prototypes.append(tmp)
                        x.append(prototypes)
                y.append(x)
            self.wave_fuction.append(y)

    def wfc(self):
        while not self.is_collapsed():
            self.check()
            self.print()
            self.iterate()

    def is_collapsed(self):
        for _y in range(self.sizeY):
            for _z in range(self.sizeZ):
                for _x in range(self.sizeX):
                    if len(self.wave_fuction[_y][_z][_x]) > 1:
                        return False
        print("finished")
        return True

    def not_collapsed_cnt(self):
        cnt = 0
        for _y in range(self.sizeY):
            for _z in range(self.sizeZ):
                for _x in range(self.sizeX):
                    if len(self.wave_fuction[_y][_z][_x]) > 1:
                        cnt += 1
        return cnt

    def iterate(self):
        x = 0
        y = 0
        z = 0
        min_entropy = 100

        for _y in range(self.sizeY):
            for _z in range(self.sizeZ):
                for _x in range(self.sizeX):
                    if(1 < len(self.wave_fuction[_y][_z][_x]) < min_entropy):
                        min_entropy = len(self.wave_fuction[_y][_z][_x])
                        x = _x
                        y = _y
                        z = _z

        self.wave_fuction[y][z][x] = self.collapse(self.wave_fuction[y][z][x])

        print(self.not_collapsed_cnt())

    def collapse(self, cell):
        tmp = []
        tmp.append(random.choice(cell))
        return tmp

    # def check(self):
    #     print("check")
    #     for _y in range(0, 1):
    #         for _z in range(1, self.sizeZ-1):
    #             for _x in range(1, self.sizeX-1):
    #                 if len(self.wave_fuction[_y][_z][_x]) > 1:
    #                     for p in self.wave_fuction[_y][_z][_x]:
    #                         for nL in self.wave_fuction[_y][_z][_x-1]:
    #                             if nL.name not in p.L:
    #                                 try:
    #                                     self.wave_fuction[_y][_z][_x].remove(p)
    #                         for nR in self.wave_fuction[_y][_z][_x+1]:
    #                             if nR.name not in p.R:
    #                                 try:
    #                                     self.wave_fuction[_y][_z][_x].remove(p)
    #                         for nF in self.wave_fuction[_y][_z-1][_x]:
    #                             if nF.name not in p.F:
    #                                 try:
    #                                     self.wave_fuction[_y][_z][_x].remove(p)
    #                         for nB in self.wave_fuction[_y][_z+1][_x]:
    #                             if nB.name not in p.B:
    #                                 try:
    #                                     self.wave_fuction[_y][_z][_x].remove(p)

    def check(self):
        print("check")
        for _y in range(0, 1):
            for _z in range(1, self.sizeZ-1):
                for _x in range(1, self.sizeX-1):
                    if len(self.wave_fuction[_y][_z][_x]) > 1:
                        for p in self.wave_fuction[_y][_z][_x]:
                            for nL in self.wave_fuction[_y][_z][_x-1]:
                                if nL.name in p.L:
                                    break
                                    try:
                                        self.wave_fuction[_y][_z][_x].remove(p)
                                    except:
                                        pass
                            for nR in self.wave_fuction[_y][_z][_x+1]:
                                if nR.name in p.R:
                                    break
                                else:
                                    try:
                                        self.wave_fuction[_y][_z][_x].remove(p)
                                    except:
                                        pass
                            for nF in self.wave_fuction[_y][_z-1][_x]:
                                if nF.name in p.F:
                                    break
                                else:
                                    try:
                                        self.wave_fuction[_y][_z][_x].remove(p)
                                    except:
                                        pass
                            for nB in self.wave_fuction[_y][_z+1][_x]:
                                if nB.name not in p.B:
                                    break
                                else:
                                    try:
                                        self.wave_fuction[_y][_z][_x].remove(p)
                                    except:
                                        pass

    def print(self):
        for _y in range(self.sizeY):
            for _z in range(self.sizeZ):
                for _x in range(self.sizeX):
                    if len(self.wave_fuction[_y][_z][_x]) >1:
                        print ("----",end=" ")
                    else:
                        print(self.wave_fuction[_y][_z][_x][0].name, end=" ")
                print("")


if __name__ == "__main__":

    Directions = ["L", "R", "F", "B"]

    # print (prototypes[0].L)
    B = Building(10, 10, 1)
    #print(B.wave_fuction[0][1][1][1].name not in B.wave_fuction[0][1][1][2].L)
    # for _y in range(B.sizeY):
    #         for _z in range(B.sizeZ):
    #             for _x in range(B.sizeX):
    #                 print(B.wave_fuction[_y][_z][_x][1].getPos())
    B.wfc()
    B.print()

