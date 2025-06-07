import time
import math
import glob
import random

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage

import trackFromBmpReader
from car import Car

import saveRouteToFile


class VectorRaceModel():
    UPDATE_RELOAD_MODEL_ITEMS = 0
    
    def __init__(self, trackName):
        self.viewLayerManager = None
        self.trackName = trackName
        self.track = None
        self.restart()

    
    def restart(self):
        self.loadWorld(self.trackName)
        self.loadPlayers()

        if(self.viewLayerManager != None):
            self.viewLayerManager.notify(self.UPDATE_RELOAD_MODEL_ITEMS)
        

    def loadWorld(self, track):
        self.track = trackFromBmpReader.importTrackByName(track)        


    def loadPlayers(self):
        self.playerliste = []
        
        # Spieler
        carPlayer = Car("Paul", self.track.startSpots["1"])
        itemPlayer = QGraphicsPixmapItem((QPixmap.fromImage(QImage("imgTestPlayer.bmp"))))
        carPlayer.setGfxItem(itemPlayer, worldScale=15)
        self.playerliste.append(carPlayer)
        
        # Gegenspieler
        carsOthers = self.loadGhostPlayers()
        for c in carsOthers:
            self.playerliste.append(c)
        

    def save(self):
        saveRouteToFile.saveRouteToFile(track=self.track, name=self.getPlayer().name, poses=self.getPlayer().moves)


    def getPlayer(self):
        return self.playerliste[0]
    
    
    def getGhost(self):
        return self.playerliste[1]
    

    def setPlayerName(self, name):
        self.getPlayer().name = name
        
        
    def loadGhostPlayers(self):
        
        others = []
        
        savFiles = []
        for file in glob.glob("tracks/" + self.track.name + "/*.sav"):
            savFiles.append(file)
        
        cnt = len(savFiles)
        if(cnt > 0):
            savId = random.randint(0,cnt-1)
            d = saveRouteToFile.loadRouteFromFile(savFiles[savId])
            if(d):
                trajectory = d["zuege"]
                ghost = Car(name=d["name"] + " (" + savFiles[savId] + ")", pos=trajectory[0])
                ghost.setTrajectory(trajectory)
                
                itemGhost = QGraphicsPixmapItem((QPixmap.fromImage(QImage("imgTestGhost.bmp"))))
                ghost.setGfxItem(itemGhost, worldScale=15)
                
                others.append(ghost)
                
        return others



    def movePlayer(self, newPos):
        self.getPlayer().move(newPos=newPos)
        
        # Move Ghosts
        for i in range(1, len(self.playerliste)):
            self.playerliste[i].stepTrajectory()
            
            
            

    def update_model(self):
        pass


    def setView(self, viewLayerManager):
        self.viewLayerManager = viewLayerManager