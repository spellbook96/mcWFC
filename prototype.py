
class Prototype:
    def __init__(self,PList,size,level):
        self.PList =PList
        self.n = len(PList)
        self.level =level
        self.size = size

    def show(self,x,y,z,redo = 10,num = 10):
        if num ==0:
            num = self.n
        if num > self.n:
            print("n must less than %d" % self.n)
            return False
        
        space = 0
        for prototype in self.PList[:num]:
            for _y in range(self.size):
                for _z in range(self.size):
                    for _x in range(self.size):
                        self.level.setBlock(_x+x+space,_y+y,_z+z,prototype[_y][_z][_x])
                    
            space+=(self.size+1)

        self.level.flush()
        import time
        time.sleep(10)
        print("undo")
        self.level.undo()
