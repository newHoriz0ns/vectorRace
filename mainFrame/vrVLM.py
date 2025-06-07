
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsScene
from PyQt5.QtGui import QPen, QBrush, QColor

"""
!!! EXAMPLE !!!

author: Paul
version: v0.2
lastChange: 31.7.23

Koordination von Layern (Views) mit Widgets und Daten

# Layout
# Widgets in Layout zur Darstellung von Inhalten
# Einfache Funktionen zum ändern von Werten in Inhalten
# Aktualisierug der Inhalte durch Widgets


"""

from vrModel import VectorRaceModel
from viewLayerPlay import ViewLayerPlay

class VectorRaceVLM():

    # STATES
    STATE_PLAY = 0

    # VIEW_IDs
    VIEW_PLAY = 0



    def __init__(self, model: VectorRaceModel):
        self.m = model
        self.vc = None                      # ViewContainer
        self.state = self.STATE_PLAY


    def set_viewContainer(self, view):
        self.vc = view
        # Initialisiere Views
        self.init_views()
        # Aktiviere aktuelle View
        self.update_viewLayout()


    def init_views(self):
        
        self.vlPlay = ViewLayerPlay(self.m)
        self.vc.add_view(self.VIEW_PLAY, self.vlPlay)


    def notify(self, _id):
        if(_id == VectorRaceModel.UPDATE_RELOAD_MODEL_ITEMS):
            self.vlPlay.weltView.wgs.reloadItems()


    def update_vlm(self):
        self.vlPlay.updateView()



    def update_viewLayout(self):
        """
        Entsprechned aktuellem self.state wird layout der View angepasst.
        """

        if(self.state == self.STATE_PLAY):
            self.vc.set_currentView(self.VIEW_PLAY)
        else:
            print ("What")


    def toggleState(self):
        self.update_viewLayout()


################
# EVENT Handler
#

    def handleKeyPress(self, e):
        pass

    def handleKeyRelease(self, e):
        # Auto steuern
        dir = None
        if(e.key() == 16777233):
            dir = [-1,1]
        elif(e.key() == 16777237):
            dir = [0,1]
        elif(e.key() == 16777239):
            dir = [1,1]
        elif(e.key() == 16777234):
            dir = [-1,0]
        elif(e.key() == 16777227):
            dir = [0,0]
        elif(e.key() == 16777236):
            dir = [1,0]
        elif(e.key() == 16777232):
            dir = [-1,-1]
        elif(e.key() == 16777235):
            dir = [0,-1]
        elif(e.key() == 16777238):
            dir = [1,-1]
        if(dir != None):
            newPos = [self.m.getPlayer().pos[0] + self.m.getPlayer().lastMove[0] + dir[0], self.m.getPlayer().pos[1] + self.m.getPlayer().lastMove[1] + dir[1]]
            self.m.movePlayer(newPos)


        if(e.key() == 83):  # s
            self.m.save()