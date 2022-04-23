#!/usr/bin/python
# -*- coding: UTF-8 -*-


from building.roofBuilder import RoofBuilder

class Shrine_Builder:

    #door == 0->front 1->back
    

    def __init__(self, level, start_x, start_y, start_z, direction, tree_ID,tree_data,wood_ID,wood_data,roof_ID):
        self.level = level
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.direction = direction
        self.tree_ID = tree_ID
        self.tree_data = tree_data
        self.wood_ID = wood_ID
        self.wood_data = wood_data
        self.roof_ID = roof_ID

    def build(self):
        lv = self.level
        x = self.start_x
        y = self.start_y
        z = self.start_z
        di = self.direction
        t_ID =self.tree_ID
        t_data =self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID
        w = 9
        d = 15
        


        def wallX(x,y,z,s):
            if di==0:
                for j in range(1,16): #line_W
                    if(j==1 or j==5 or j==11 or j==15):
                        for k in range(1,13): #line_H
                            self.level.setBlockID(x,y+k,z+j,t_ID,t_data)#black
                    else:
                        for k in range(1,13): #line_H
                            if k==5:
                                self.level.setBlockID(x,y+k,z+j,t_ID,t_data)#black
                            else:
                                self.level.setBlockID(x,y+k,z+j,96,s)
                        for k in range(6,9): 
                            self.level.setBlockID(x,y+k,z+j,w_ID,w_data)#white
                        for k in range(10,13):
                            self.level.setBlockID(x,y+k,z+j,96,s)
                        if(j==3 or j==8 or j==13):
                            self.level.setBlockID(x,y+2,z+j,196,0)#door
                            self.level.setBlockID(x,y+3,z+j,196,8)#door
            if di==1:
                for j in range(1,16): #line_W
                    if(j==1 or j==5 or j==11 or j==15):
                        for k in range(1,13): #line_H
                            self.level.setBlockID(x+j,y+k,z,t_ID,t_data)#black
                    else:
                        for k in range(1,13): #line_H
                            if k==5:
                                self.level.setBlockID(x+j,y+k,z,t_ID,t_data)#black
                            else:
                                self.level.setBlockID(x+j,y+k,z,96,s)
                        for k in range(6,9): 
                            self.level.setBlockID(x+j,y+k,z,w_ID,w_data)#white
                        for k in range(10,13):
                            self.level.setBlockID(x+j,y+k,z,96,s)
                        if(j==3 or j==8 or j==13):
                            self.level.setBlockID(x+j,y+2,z,196,1)#door
                            self.level.setBlockID(x+j,y+3,z,196,9)#door              
            
        def wallZ(x,y,z,s):
            if di==0:
                for j in range(0,8): #line_W
                    self.level.setBlockID( x + j, y+1, z, t_ID,t_data)#black
                    self.level.setBlockID( x+j, y+13, z, t_ID,t_data)#black
                    if(j==0 or j==4 or j==8):
                        for k in range(1,14): #line_H
                            self.level.setBlockID( x + j, y + k, z, t_ID,t_data)#black
                    else:
                        for k in range(2,13): #line_H
                            if k==5:
                                self.level.setBlockID( x + j, y + k, z, t_ID,t_data)#black
                            else:
                                self.level.setBlockID(x+j,y+k,z,96,s)
                        for k in range(6,9): 
                            self.level.setBlockID(x+j,y+k,z,w_ID,w_data)#white
                        for k in range(10,13):
                            self.level.setBlockID(x+j,y+k,z,96,s)
            if di==1:
                for j in range(0,8): #line_W
                    self.level.setBlockID( x, y+1, z+j, t_ID,t_data)#black
                    self.level.setBlockID( x, y+13, z+j, t_ID,t_data)#black
                    if(j==0 or j==4 or j==8):
                        for k in range(1,14): #line_H
                            self.level.setBlockID( x, y + k, z+j, t_ID,t_data)#black
                    else:
                        for k in range(2,13): #line_H
                            if k==5:
                                self.level.setBlockID( x, y + k, z+j, t_ID,t_data)#black
                            else:
                                self.level.setBlockID(x,y+k,z+j,96,s)
                        for k in range(6,9): 
                            self.level.setBlockID(x,y+k,z+j,w_ID,w_data)#white
                        for k in range(10,13):
                            self.level.setBlockID(x,y+k,z+j,96,s)


        def roof(x,s,z,t):
            if di==0:  
                for i in range(0, 4):
                    for j in range(x-4+i, x + 9 + 4-i):    # left
                        if i == 0:
                            self.level.setBlockID( j, s-1, z - 4 + i, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(x-4+i, x + 9 + 4-i):  # right
                        if i == 0:
                            self.level.setBlockID( j, s-1, z + d + 3 - i, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( j, s, z + d + 3 - i, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( j, s, z + d + 3 - i, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( j, s, z + d + 3 - i, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(z-4+i, z + d + 3 - i):  # under
                        if i == 0:
                            self.level.setBlockID( x - 4 + i, s - 1, j, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(z-4+i, z + d + 3 - i):  # under
                        if i == 0:
                            self.level.setBlockID( x + d + 3 - i-6, s - 1, j,r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( x + d + 3 - i-6, s, j, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( x + d + 3 - i-6, s, j, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( x + d + 3 - i-6, s, j, r_ID[1], r_ID[2]+8)
            if di==1:  
                for i in range(0, 4):
                    for j in range(z-4+i, z + 9 + 4-i):    # left
                        if i == 0:
                            self.level.setBlockID( x - 4 + i, s-1, j, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( x - 4 + i, s, j, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(z-4+i, z + 9 + 4-i):  # right
                        if i == 0:
                            self.level.setBlockID( x + d + 3 - i, s-1, j, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( x + d + 3 - i, s, j, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( x + d + 3 - i, s, j, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( x + d + 3 - i, s, j, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(x-4+i, x + d + 3 - i):  # under
                        if i == 0:
                            self.level.setBlockID( j, s - 1, z - 4 + i, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( j, s, z - 4 + i, r_ID[1], r_ID[2]+8)
                for i in range(0, 4):
                    for j in range(x-4+i, x + d + 3 - i):  # under
                        if i == 0:
                            self.level.setBlockID( j, s - 1, z + d + 3 - i-6, r_ID[1], r_ID[2]+8)
                        elif i == 1:
                            self.level.setBlockID( j, s, z + d + 3 - i-6, r_ID[1], r_ID[2])
                        elif i == 2:
                            self.level.setBlockID( j, s, z + d + 3 - i-6, r_ID[3], r_ID[4])
                        else:
                            self.level.setBlockID( j, s, z + d + 3 - i-6, r_ID[1], r_ID[2]+8)

        def floor(x,y,z,t_ID,t_data):
            if di==0:
                for j in range(17):
                    for i in range(1,16):
                        self.level.setBlockID(x+i,y+1,z+j,126,0)
                        if j==0 or j==16:
                            self.level.setBlockID(x+i,y,z+j,85,0)
                            self.level.setBlockID(x+i,y,z+j,85,0)
                        if i==1 or i==15:
                            self.level.setBlockID(x+i,y,z+j,85,0)
                            self.level.setBlockID(x+i,y,z+j,85,0)
                for j in range(1,16):
                    self.level.setBlockID(x+4,y+1,z+j, t_ID,t_data)
                    self.level.setBlockID(x+12,y+1,z+j,t_ID,t_data)
                for i in range(4,12):
                    self.level.setBlockID(x+i,y+1,z+15,t_ID,t_data)
                    self.level.setBlockID(x+i,y+1,z+1,t_ID,t_data)
                for k in range(7,10):
                    self.level.setBlockID(x,y,z+k,53,0)#stears
                    self.level.setBlockID(x+16,y,z+k,53,1)
                    self.level.setBlockID(x+2,y+1,z+k,t_ID,t_data)#sa==en box
                    self.level.setBlockID(x+2,y+2,z+k,96,0)
                    self.level.setBlockID(x+14,y+1,z+k,t_ID,t_data)#sa==en box
                    self.level.setBlockID(x+14,y+2,z+k,96,0)
                self.level.setBlockID(x+5,y+2,z+2,89,0)#glowStone
                self.level.setBlockID(x+11,y+2,z+2,89,0)#glowStone
                self.level.setBlockID(x+5,y+2,z+14,89,0)#glowStone
                self.level.setBlockID(x+11,y+2,z+14,89,0)#glowStone
                self.level.setBlockID(x+4,y+12,z+2,89,0)#glowStone
                self.level.setBlockID(x+11,y+12,z+2,89,0)#glowStone
                self.level.setBlockID(x+4,y+12,z+14,89,0)#glowStone
            elif di==1:
                for j in range(17):
                    for i in range(1,16):
                        self.level.setBlockID(x+j,y+1,z+i,126,0)
                        if j==0 or j==16:
                            self.level.setBlockID(x+j,y,z+i,85,0)
                            self.level.setBlockID(x+j,y,z+i,85,0)
                        if i==1 or i==15:
                            self.level.setBlockID(x+j,y,z+i,85,0)
                            self.level.setBlockID(x+j,y,z+i,85,0)
                for j in range(1,16):
                    self.level.setBlockID(x+j,y+1,z+4,t_ID,t_data)
                    self.level.setBlockID(x+j,y+1,z+12,t_ID,t_data)
                for i in range(4,12):
                    self.level.setBlockID(x+15,y+1,z+i,t_ID,t_data)
                    self.level.setBlockID(x+1,y+1,z+i,t_ID,t_data)
                for k in range(7,10):
                    self.level.setBlockID(x+k,y,z,53,2)#stears
                    self.level.setBlockID(x+k,y,z+16,53,3)
                    self.level.setBlockID(x+k,y+1,z+2,t_ID,t_data)#sa==en box
                    self.level.setBlockID(x+k,y+2,z+2,96,0)
                    self.level.setBlockID(x+k,y+1,z+14,t_ID,t_data)#sa==en box
                    self.level.setBlockID(x+k,y+2,z+14,96,0)
                self.level.setBlockID(x+2,y+2,z+5,89,0)#glowStone
                self.level.setBlockID(x+2,y+2,z+11,89,0)#glowStone
                self.level.setBlockID(x+14,y+2,z+5,89,0)#glowStone
                self.level.setBlockID(x+14,y+2,z+11,89,0)#glowStone
                self.level.setBlockID(x+2,y+12,z+4,89,0)#glowStone
                self.level.setBlockID(x+2,y+12,z+11,89,0)#glowStone
                self.level.setBlockID(x+14,y+12,z+4,89,0)#glowStone
                self.level.setBlockID(x+14,y+12,z+11,89,0)#glowStone
            

            
            
        if di==0:
            sx=7
            sz=5
            for i in range(17):
                    for j in range(15):
                        for k in range(23):
                            self.level.setBlockID(x+i,y+j,z-3+k,0,0)
            wallZ(x+4,y,z+1,sz) #x,z
            wallZ(x+4,y,z+15,sz) #x,z
            wallX(x+4,y,z,sx) #x,y,z,door,s
            wallX(x+12,y,z,sx) #x,y,z,door,s
            r = RoofBuilder(lv, x+4, z+1, d, y+13, di, 0, t_ID,t_data,w_ID,w_data,r_ID)
            r.build()
            roof(x+4,y+8,z+1,1)
        elif di==1:
            sx=5
            sz=7
            for i in range(17):
                    for j in range(9):
                        for k in range(23):
                            self.level.setBlockID(x-3+k,y+j,z+i,0,0)
            wallZ(x+1,y,z+4,sz) #x,z
            wallZ(x+15,y,z+4,sz) #x,z
            wallX(x,y,z+4,sx) #x,y,z,door,s
            wallX(x,y,z+12,sx) #x,y,z,door,s
            r = RoofBuilder(lv, x+1, z+4, d, y+13, di, 0, t_ID,t_data,w_ID,w_data,r_ID)
            r.build()
            roof(x+1,y+8,z+4,1)
        floor(x,y,z,t_ID,t_data)