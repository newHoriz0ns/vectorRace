import time
import math
import glob
import random

from PyQt5.QtWidgets import QGraphicsPixmapItem, QMessageBox
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

    
    def changeTrack(self, newTrack):
        self.trackName = newTrack
        self.restart()
        
    
    def changeGhost(self, ghost):
        pass
    
    
    def restart(self):
        self.loadWorld(self.trackName)
        self.loadPlayers()

        if(self.viewLayerManager != None):
            self.viewLayerManager.notify(self.UPDATE_RELOAD_MODEL_ITEMS)
        

    def loadWorld(self, track):
        self.track = trackFromBmpReader.importTrackByName(track)    
        self.trackName = self.track.name    


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
        
        maxCntGhosts = 5
        i = 1
        for s in savFiles:
            if(i <= maxCntGhosts):
                d = saveRouteToFile.loadRouteFromFile(s)
                if(d):
                    trajectory = d["zuege"]
                    ghost = Car(name=d["name"] + " (" + s + ")", pos=trajectory[0])
                    ghost.setTrajectory(trajectory)
                    
                    itemGhost = QGraphicsPixmapItem((QPixmap.fromImage(QImage(f"cars/imgTestGhost{i}.bmp"))))
                    ghost.setGfxItem(itemGhost, worldScale=15)
                    
                    others.append(ghost)
                    i += 1
                
        return others



    def movePlayer(self, newPos):
        self.getPlayer().move(newPos=newPos)
        
        # Move Ghosts
        for i in range(1, len(self.playerliste)):
            self.playerliste[i].stepTrajectory()
            
        self.checkCrash()
            
    
    def checkCrash(self):
        pos = self.getPlayer().pos
        crash = True
        try:
            crash = self.track.karte[pos[1]][pos[0]] == trackFromBmpReader.MAP_WALL
        except:
            crash = True    
        
        if(crash):
            # Crash
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Crash!!!")
            msg.setText("Game Over!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.button(QMessageBox.Ok).setText("Neustart")
            result = msg.exec_()
            if result == QMessageBox.Ok:
                self.restart()
            else:
                self.restart()   
            

    def update_model(self):
        pass


    def setView(self, viewLayerManager):
        self.viewLayerManager = viewLayerManager