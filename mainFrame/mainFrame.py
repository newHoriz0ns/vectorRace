"""
author: Paul
version: v0.2
lastChange: 31.7.23
"""

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeyEvent

from PyQt5.QtWidgets import QMainWindow

import mainFrame.viewContainer as vc
from vrModel import VectorRaceModel

class MainFrame(QMainWindow):

    def __init__(self, model:VectorRaceModel):
        super().__init__()

        # ViewContainer
        self.view = vc.ViewContainer()
        self.setCentralWidget(self.view)

        self.m = model

        # ViewLayerManager (wird nach Initialisierung von main aus per set_viewLayerManager gesetzt)
        self.vlm = None


    def init_updateRoutine(self):
        """
        Initialisierung durch Main
        """
        self.updateTimer = QTimer()
        self.updateTimer.setTimerType(Qt.PreciseTimer)
        self.updateTimer.setInterval(0) # Wird durch vsync gesteuert
        self.updateTimer.timeout.connect(self.vlm.update_vlm, Qt.DirectConnection)
        self.updateTimer.timeout.connect(self.m.update_model)


    def start_updateRoutine(self):
        """
        Start durch Main
        """
        self.updateTimer.start()
        

    def set_viewLayerManager(self, vlm):
        self.vlm = vlm


    def set_viewLayout(self, layout, structure):
        """
        Übergibt die neue Struktur an die MainView
        """
        self.view.set_layout(layout, structure)



    #################
    # EVENT HANDLER
    #


    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.vlm.handleKeyPress(a0)
        return super().keyPressEvent(a0)
    
    
    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        self.vlm.handleKeyRelease(a0)
        return super().keyReleaseEvent(a0)