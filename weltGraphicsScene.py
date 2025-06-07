from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsTextItem
from PyQt5.QtGui import QColor, QBrush, QKeyEvent, QPen, QPixmap, QImage, QFont

from vrModel import VectorRaceModel
import trackFromBmpReader

SCALE_FACTOR = 15   # Pixel pro Feld

class WeltGraphicsScene(QGraphicsScene):


    def __init__(self, m: VectorRaceModel):
        super().__init__()
        
        self.m = m

        # Model Items
        self.reloadItems()

        
        # Setze Fokus auf (centerOn durch testView)
        # self.set_centerItem(self.itemPlayer)
        

    def reloadItems(self):

        self.clear()

        # StatusMsg 
        self.itemText = QGraphicsTextItem("")
        self.itemText.setPos(0, -25)
        font = QFont("Arial", 8, QFont.Normal)
        self.itemText.setFont(font)
        self.addItem(self.itemText)

        self.loadTrackTiles()
        self.loadPossibleMoveTiles()

        # Ghost
        for i in range (1,len(self.m.playerliste)):
            self.addItem(self.m.playerliste[i].gfxItem)
            self.set_statusText(self.m.getGhost().name)

        # Player 
        self.addItem(self.m.getPlayer().gfxItem)
        



    def loadTrackTiles(self):

        self.imgWand = QImage("imgTestWand.bmp")
        self.imgStrasse = QImage("imgTestStrasse.bmp")
        self.imgStart = QImage("imgTestStart.bmp")
        self.imgZiel = QImage("imgTestZiel.bmp")

        for y in range(len(self.m.track.karte)):
            for x in range(len(self.m.track.karte[y])):

                if(self.m.track.karte[y][x] == trackFromBmpReader.MAP_SREET):
                    item = QGraphicsPixmapItem(QPixmap.fromImage(self.imgStrasse))
                if(self.m.track.karte[y][x] == trackFromBmpReader.MAP_WALL):
                    item = QGraphicsPixmapItem(QPixmap.fromImage(self.imgWand))
                if(self.m.track.karte[y][x] == trackFromBmpReader.MAP_START):
                    item = QGraphicsPixmapItem(QPixmap.fromImage(self.imgStart))
                if(self.m.track.karte[y][x] == trackFromBmpReader.MAP_ZIEL):
                    item = QGraphicsPixmapItem(QPixmap.fromImage(self.imgZiel))
        
                item.setPos(x * SCALE_FACTOR, y * SCALE_FACTOR)
                self.addItem(item)



    def loadPossibleMoveTiles(self):
        self.possibleMoveItems:QGraphicsRectItem = []
        for i in range(9):
            item = PossibleMoveItem(self)
            self.possibleMoveItems.append(item)
            self.addItem(item)


    def update_graphicsScene(self):
        self.show_possibleMoves()




    def show_possibleMoves(self):
        i = 0
        for p in self.m.getPlayer().nextPossible:
            self.possibleMoveItems[i].setPos(p[0] * SCALE_FACTOR + 1, p[1] * SCALE_FACTOR + 1)
            i = i + 1


    def centerItem(self):
        return self.__centerItem
    
    
    def set_centerItem(self, item):
        self.__centerItem = item
        
        
    def set_statusText(self, text):
        self.itemText.setHtml("<p style='color:blue'>" + text + "</p>")
        




class PossibleMoveItem(QGraphicsRectItem):
    
    def __init__(self, scene : WeltGraphicsScene):
        super().__init__(QtCore.QRectF(0, 0, SCALE_FACTOR - 2, SCALE_FACTOR - 2))
        self.setPen(QtCore.Qt.red)
        self.s = scene
        self.m = scene.m


    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.m.movePlayer(newPos=[int(self.pos().x() / SCALE_FACTOR), int(self.pos().y() / SCALE_FACTOR)])
        return super().mouseDoubleClickEvent(event)