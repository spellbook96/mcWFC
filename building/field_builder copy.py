from numpy import *
import random


class field:

    def __init__(self, level, start_x, start_y, start_z, size_x, size_z, field_type, letter_type):
            self.level = level
            self.start_x = start_x
            self.start_y = start_y
            self.start_z = start_z
            self.size_x = size_x
            self.size_z = size_z
            self.field_type = field_type
            self.letter_type = letter_type

    def build(self):
        lv = self.level
        x = self.start_x
        y = self.start_y
        z = self.start_z
        s_x = self.size_x
        s_z = self.size_z
        l_type = self.letter_type

        plant = ["minecraft:carrots[age=7]","minecraft:potatoes[age=7]","minecraft:wheat[age=7]"]
        l_ID = ["minecraft:jack_o_lantern","minecraft:blue_stained_glass","minecraft:water"]
        r = random.randint(0,8)
        s = random.randint(0,2)
        flower = ["poppy","blue_orchid","allium","azure_bluet","red_tulip","orange_tulip","white_tulip","pink_tulip","oxeye_daisy"]
        if self.field_type == 0:
            for i in range(s_x):
                for j in range(s_z):
                    self.level.setBlock(x+i, y, z+j,"minecraft:grass")
                    self.level.setBlock(x+i, y+1, z+j,"minecraft:oak_fence")
            for i in range(1, s_x-1):
                for j in range(1, s_z-1):
                    self.level.setBlock(x+i, y, z+j, "minecraft:farmland[moisture=7]")
                    #your favorite plants
                    self.level.setBlock(x+i, y+1, z+j, plant[s]) 
                self.level.setBlock(x+s_x/2, y+1, z-1,"air")
            self.level.setBlock(x+1, y, z+1,"minecraft:water")#water
            self.level.setBlock(x+1, y, z+s_z-2,"minecraft:water")
            self.level.setBlock(x+s_x-2, y, z+1,"minecraft:water")
            self.level.setBlock(x+s_x-2, y, z+s_z-2,"minecraft:water")
            self.level.setBlock(x+1, y+1, z+1,"air")#air
            self.level.setBlock(x+1, y+1, z+s_z-2,"air")
            self.level.setBlock(x+s_x-2, y+1, z+1,"air")
            self.level.setBlock(x+s_x-2, y+1, z+s_z-2,"air")
            self.level.setBlock(x, y+1, z+s_z/2,"air")#air
            self.level.setBlock(x+s_x-1, y+1, z+s_z/2,"air")#air
            if s_z>9:
                self.level.setBlock(x+s_x/2, y, z+s_z/2,"minecraft:water")#water
                self.level.setBlock(x+s_x/2, y+1, z+s_z/2,"air")#air

        elif self.field_type == 1:#I
            letter = [[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,1,1,1,1,1,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    self.level.setBlock(x+i, y, z+j,"minecraft:grass")
                    self.level.setBlock(x+i, y+1, z+j,"minecraft:oak_fence")
            for i in range(7):
                for j in range(7):
                    self.level.setBlock(x+i+1, y, z+j+1,"minecraft:farmland[moisture=7]")
                    if letter[j][i]==0:
                        self.level.setBlock(x+i+1, y+1, z+j+1,flower[r])
                    elif letter[j][i]==1:
                        if l_type==2:
                            self.level.setBlock(x+i+1, y-1, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y, z+j+1, l_ID[l_type]) #letter
                            self.level.setBlock(x+i+1, y+1, z+j+1,"air") #air
                        else:
                            self.level.setBlock(x+i+1, y, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y+1, z+j+1, l_ID[l_type]) #letter
                self.level.setBlock(x+9/2, y+1, z-1,"air")
            self.level.setBlock(x+1, y, z+1,"minecraft:water")#water
            self.level.setBlock(x+1, y, z+7,"minecraft:water")
            self.level.setBlock(x+7, y, z+1,"minecraft:water")
            self.level.setBlock(x+7, y, z+7,"minecraft:water")
            self.level.setBlock(x+1, y+1, z+1,"air")#air
            self.level.setBlock(x+1, y+1, z+7,"air")
            self.level.setBlock(x+7, y+1, z+1,"air")
            self.level.setBlock(x+7, y+1, z+7,"air")
            self.level.setBlock(x, y+1, z+s_z/2,"air")#air
            self.level.setBlock(x+s_x-1, y+1, z+s_z/2,"air")#air
        elif self.field_type == 2:#C
            letter = [[0,0,0,0,0,0,0],[0,0,1,1,1,0,0],[0,1,0,0,0,1,0],[0,1,0,0,0,0,0],[0,1,0,0,0,1,0],[0,0,1,1,1,0,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    self.level.setBlock(x+i, y, z+j,"minecraft:grass")
                    self.level.setBlock(x+i, y+1, z+j,"minecraft:oak_fence")
            for i in range(7):
                for j in range(7):
                    self.level.setBlock(x+i+1, y, z+j+1,"minecraft:farmland[moisture=7]")
                    if letter[j][i]==0:
                        self.level.setBlock(x+i+1, y+1, z+j+1,flower[r])
                    elif letter[j][i]==1:
                        if l_type==2:
                            self.level.setBlock(x+i+1, y-1, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y, z+j+1, l_ID[l_type]) #letter
                            self.level.setBlock(x+i+1, y+1, z+j+1,"air") #air
                        else:
                            self.level.setBlock(x+i+1, y, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y+1, z+j+1, l_ID[l_type]) #letter
                self.level.setBlock(x+9/2, y+1, z-1,"air")
            self.level.setBlock(x+1, y, z+1,"minecraft:water")#water
            self.level.setBlock(x+1, y, z+7,"minecraft:water")
            self.level.setBlock(x+7, y, z+1,"minecraft:water")
            self.level.setBlock(x+7, y, z+7,"minecraft:water")
            self.level.setBlock(x+1, y+1, z+1,"air")#air
            self.level.setBlock(x+1, y+1, z+7,"air")
            self.level.setBlock(x+7, y+1, z+1,"air")
            self.level.setBlock(x+7, y+1, z+7,"air")
            self.level.setBlock(x, y+1, z+s_z/2,"air")#air
            self.level.setBlock(x+s_x-1, y+1, z+s_z/2,"air")#air
        elif self.field_type == 3:#E
            letter = [[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,0,0,0,0,0],[0,1,1,1,1,1,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    self.level.setBlock(x+i, y, z+j,"minecraft:grass")
                    self.level.setBlock(x+i, y+1, z+j,"minecraft:oak_fence")
            for i in range(7):
                for j in range(7):
                    self.level.setBlock(x+i+1, y, z+j+1,"minecraft:farmland[moisture=7]")
                    if letter[j][i]==0:
                        self.level.setBlock(x+i+1, y+1, z+j+1,flower[r])
                    elif letter[j][i]==1:
                        if l_type==2:
                            self.level.setBlock(x+i+1, y-1, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y, z+j+1, l_ID[l_type]) #letter
                            self.level.setBlock(x+i+1, y+1, z+j+1,"air") #air
                        else:
                            self.level.setBlock(x+i+1, y, z+j+1,"minecraft:glowstone") #glowstone
                            self.level.setBlock(x+i+1, y+1, z+j+1, l_ID[l_type]) #letter
                self.level.setBlock(x+9/2, y+1, z-1,"air")
            self.level.setBlock(x+1, y, z+1,"minecraft:water")#water
            self.level.setBlock(x+1, y, z+7,"minecraft:water")
            self.level.setBlock(x+7, y, z+1,"minecraft:water")
            self.level.setBlock(x+7, y, z+7,"minecraft:water")
            self.level.setBlock(x+1, y+1, z+1,"air")#air
            self.level.setBlock(x+1, y+1, z+7,"air")
            self.level.setBlock(x+7, y+1, z+1,"air")
            self.level.setBlock(x+7, y+1, z+7,"air")
            self.level.setBlock(x, y+1, z+s_z/2,"air")#air
            self.level.setBlock(x+s_x-1, y+1, z+s_z/2,"air")#air
    
        elif self.field_type == 4:#suger
            y-=1
            for i in range(s_x):
                for j in range(s_z):
                    if i%2==0:
                        #your favorite plants
                        self.level.setBlock(x+i, y, z+j,"minecraft:sand") 
                        self.level.setBlock(x+i, y+1, z+j,"sugar_cane[age=7]") 
                        self.level.setBlock(x+i, y+2, z+j,"sugar_cane[age=7]") 
                        self.level.setBlock(x+i, y+3, z+j,"sugar_cane[age=7]") 
                    else:
                        self.level.setBlock(x+i, y, z+j,"minecraft:water")
                        self.level.setBlock(x+i, y+1, z+j,"air")
                self.level.setBlock(x+s_x/2, y+3, z-1,"air")
            for j in range(1, s_z-1):
                self.level.setBlock(x+1, y+1, z+j,"air")
                self.level.setBlock(x+s_x-2, y+1, z+j,"air")
