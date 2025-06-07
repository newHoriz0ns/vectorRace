class Car():

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

        self.step = 0
        self.moves = []
        self.moves.append([self.pos[0], self.pos[1]])

        self.lastMove = [0,0]
        self.nextPossible = self.calc_possible()
        
        self.gfxItem = None
        self.worldScale = 1.0
        
        
        
    def setGfxItem(self, gfxItem, worldScale):
        self.gfxItem = gfxItem
        self.worldScale = worldScale
        self.updateGfxItem()



    def calc_possible(self):
        possible = []
        center = [self.pos[0] + self.lastMove[0], self.pos[1] + self.lastMove[1]]

        for x in range(center[0] - 1, center[0]+2):
            for y in range(center[1] - 1, center[1]+2):
                possible.append([x,y])

        return possible
    
    
    def updateGfxItem(self):
        if(self.gfxItem):
            self.gfxItem.setPos(self.pos[0] * self.worldScale, self.pos[1] * self.worldScale)

    
    def move(self, newPos):
        self.lastMove[0] = newPos[0] - self.moves[-1][0]
        self.lastMove[1] = newPos[1] - self.moves[-1][1]
        self.pos[0] = newPos[0]
        self.pos[1] = newPos[1]
        self.nextPossible = self.calc_possible()
        self.moves.append(newPos)
        self.step += 1
        self.updateGfxItem()
        
        
                
    def setTrajectory(self, trajectory):
        self.moves = trajectory
        self.step = 0
        
        
    def stepTrajectory(self):
        self.step += 1
        newPos = self.getCurrentPosition()
        self.pos[0] = newPos[0]
        self.pos[1] = newPos[1]
        self.updateGfxItem()
                
                
    def getCurrentPosition(self):
        return self.getPositionAtStep(self.step)
                
                
    def getPositionAtStep(self, step):
        return self.moves[min(max(0,step), len(self.moves) - 1)]