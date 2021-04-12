from config import Config
class Prototype:
    def __init__(self,name,config):
        self.name = name
        self.L = config.getKey(name+"L")
        self.R = config.getKey(name+"R")
        self.F = config.getKey(name+"F")
        self.B = config.getKey(name+"B")
        self.posX=-1
        self.posY=-1
        self.posZ=-1
        
    def setPos(self,Pos):
        self.posX=Pos[0]
        self.posZ=Pos[1]
        self.posY=Pos[2]

    def getPos(self):
        return [self.posX,self.posZ,self.posY]
        