from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtGui import QColor, QBrush, QKeyEvent, QPen, QPixmap, QImage, QFont

from vrModel import VectorRaceModel
import trackFromBmpReader

SCALE_FACTOR = 15   # Pixel pro Feld


class WeltGraphicsScene(QGraphicsScene):

    MAX_LINE_LENGTH = 75

    def __init__(self, m: VectorRaceModel):
        super().__init__()
        
        self.m = m
        self.m.sig_UpdateLines.connect(self.update_Lines)

        # Model Items
        self.reloadItems()

        
        

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
        for i in range (1, len(self.m.playerliste)):        # Skip player 
            self.addItem(self.m.playerliste[i].gfxItem)
            self.addItem(self.addPlayerTextItem(i, self.m.playerliste[i].name))

        # Player 
        self.itemPlayer = self.m.getPlayer().gfxItem
        self.addItem(self.itemPlayer)
        
        
        # Lines
        self.lines = Lines(self)
        self.lines.setMaximumSegmentCnt(self.MAX_LINE_LENGTH)
        
        # Setze Fokus auf (centerOn durch testView)
        # self.set_centerItem(self.itemPlayer)



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
        
                
    def update_Lines(self):
        for i, p  in enumerate(self.m.playerliste):
            lastPos = p.moves[-2]
            newPos = p.moves[-1]
            self.lines.addLineSegment(i, lastPos, newPos)


    def setMaximumLineLength(self, length):
        self.lines.setMaximumSegmentCnt(length)
        self.MAX_LINE_LENGTH = length
            

    def show_possibleMoves(self):

        # remove old
        for i in self.possibleMoveItems:
            self.removeItem(i)

        # calc new position
        i = 0
        for p in self.m.getPlayer().nextPossible:
            self.possibleMoveItems[i].setPos(p[0] * SCALE_FACTOR + 1, p[1] * SCALE_FACTOR + 1)
            self.addItem(self.possibleMoveItems[i])
            i = i + 1
        
    



    def centerItem(self):
        return self.__centerItem
    
    
    def set_centerItem(self, item):
        self.__centerItem = item
        
        
    def set_statusText(self, text):
        self.itemText.setHtml("<p style='color:blue'>" + text + "</p>")
    
    
    def addPlayerTextItem(self, nr, name):
        itemText = QGraphicsTextItem("")
        itemText.setPos(0, -25 - (25 * (nr+1)))
        font = QFont("Arial", 8, QFont.Normal)
        itemText.setFont(font)
        colorTexts = ["#00f", "#f0f", "#0ff", "#6f0", "#f60"] 
        itemText.setHtml((f"<p style='color:{colorTexts[nr-1]}'>" + name + "</p>"))
        return itemText


class PossibleMoveItem(QGraphicsRectItem):
    
    def __init__(self, scene : WeltGraphicsScene):
        super().__init__(QtCore.QRectF(0, 0, SCALE_FACTOR - 2, SCALE_FACTOR - 2))
        self.setPen(QtCore.Qt.red)
        self.s = scene
        self.m = scene.m


    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.m.movePlayer(newPos=[int(self.pos().x() / SCALE_FACTOR), int(self.pos().y() / SCALE_FACTOR)])
        return super().mouseDoubleClickEvent(event)
    
    
    
    
class Lines():   
        
    PLAYER_COLORS = [
        QColor("red"),
        QColor("blue"),
        QColor("pink"),
        QColor("cyan"),
        QColor("green"),
        QColor("orange")
    ]
    
    def __init__(self, parent):
        self.parent = parent
        self.lines = {}
        
        self.lines = {
            0:Line(self.parent, self.PLAYER_COLORS[0]),
            1:Line(self.parent, self.PLAYER_COLORS[1]),
            2:Line(self.parent, self.PLAYER_COLORS[2]),
            3:Line(self.parent, self.PLAYER_COLORS[3]),
            4:Line(self.parent, self.PLAYER_COLORS[4]),
            5:Line(self.parent, self.PLAYER_COLORS[5])
        }
    
    
    def addLineSegment(self, playerId, lastPos, newPos):
        self.lines[playerId].addLineSegment(playerId, lastPos, newPos)
        
    
    def setMaximumSegmentCnt(self, cnt):
        for l in self.lines:
            self.lines[l].setMaximumSegmentCnt(cnt)
        
        
    def resetLines(self, cnt=6):

        for k in range(cnt):
            for s in self.lines:
                s.resetLine()
        

class Line():
    
    def __init__(self, parent, color, maxSementCnt=10000):
        self.parent = parent
        self.line = []
        self.color = color
        self.maxSegmentCnt = maxSementCnt
        
        
    def setMaximumSegmentCnt(self, cnt):
        self.maxSegmentCnt = cnt
        while(len(self.line) > cnt):
            self.parent.removeItem(self.line[0])
            del self.line[0]
        
        
    def addLineSegment(self, playerId, lastPos, newPos):
        item = QGraphicsLineItem(lastPos[0] * SCALE_FACTOR + SCALE_FACTOR/2, lastPos[1] * SCALE_FACTOR + SCALE_FACTOR/2, newPos[0] * SCALE_FACTOR + SCALE_FACTOR/2, newPos[1] * SCALE_FACTOR + SCALE_FACTOR/2)
        pen = QPen(self.color, 1.0)
        item.setPen(pen)
        self.parent.addItem(item)
        self.line.append(item)
        if(len(self.line) > self.maxSegmentCnt):
            self.parent.removeItem(self.line[0])
            del self.line[0]
        
        
    def resetLine(self):
        pass