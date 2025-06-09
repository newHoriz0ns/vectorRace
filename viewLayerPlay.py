import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsScene, QLineEdit, QComboBox, QSlider, QLabel
from PyQt5.QtGui import QPen, QBrush, QColor

from weltGraphicsViewWidget import WeltGraphicsViewWidget

class ViewLayerPlay(QGroupBox):

    def __init__(self, model):

        super().__init__("VectorRace")

        self.m = model

        layout = QHBoxLayout()
        self.setLayout(layout)

        ##############
        # Left (Welt)
        
        #qgs = QGraphicsScene()
        #qgs.addRect(100,100,100,100,QPen(),QBrush(QColor(0,0,0)))
        self.weltView = WeltGraphicsViewWidget(self.m)
        layout.addWidget(self.weltView)
        
        
        ##############
        # Right (Status)
        
        self.statusGroup = QGroupBox()
        self.statusLayout = QVBoxLayout()
        self.statusGroup.setLayout(self.statusLayout)
        self.statusGroup.setFixedWidth(250)
        layout.addWidget(self.statusGroup)
        
        
        # Track
        self.statusTrackGroup = QGroupBox("Track")
        self.statusCurrTrackCombo = NoArrowComboBox()
        self.statusCurrTrackCombo.addItems(self.getTracks())
        currTrackindex = self.statusCurrTrackCombo.findText(self.m.trackName)
        self.statusCurrTrackCombo.setCurrentIndex(currTrackindex)
        self.statusCurrTrackCombo.currentTextChanged.connect(self.changeTrack)
        self.statusTrackLayout = QHBoxLayout()
        self.statusTrackGroup.setLayout(self.statusTrackLayout)
        self.statusTrackLayout.addWidget(self.statusCurrTrackCombo)
        self.statusLayout.addWidget(self.statusTrackGroup)
        
        # Name
        self.statusNameGroup = QGroupBox("Spielername")
        self.statusNameLayout = QHBoxLayout()
        self.statusNameGroup.setLayout(self.statusNameLayout)
        self.statusNameText = QLineEdit(self.m.getPlayer().name)
        self.statusNameText.textChanged.connect(self.m.setPlayerName)
        self.statusNameLayout.addWidget(self.statusNameText)
        self.statusLayout.addWidget(self.statusNameGroup)
        
        # Züge
        self.statusRundenGroup = QGroupBox("Züge")
        self.statusRundenLayout = QHBoxLayout()
        self.statusRundenGroup.setLayout(self.statusRundenLayout)
        self.statusRundenText = QLineEdit("Test")
        self.statusRundenText.setReadOnly(True)
        self.statusRundenLayout.addWidget(self.statusRundenText)
        self.statusLayout.addWidget(self.statusRundenGroup)
        
        # Ghost
        self.statusGhostGroup = QGroupBox("Ghosts")
        self.statusCurrGhostCombo = NoArrowComboBox()
        self.statusCurrGhostCombo.addItems(self.getGhosts())
        self.statusCurrGhostCombo.currentTextChanged.connect(self.changeGhost)
        self.statusGhostLayout = QHBoxLayout()
        self.statusGhostGroup.setLayout(self.statusGhostLayout)
        self.statusGhostLayout.addWidget(self.statusCurrGhostCombo)
        # self.statusLayout.addWidget(self.statusGhostGroup)        
        
        # Lines
        self.statusLinesGroup = QGroupBox("Max. Spur Länge")
        self.statusLinesLayout = QVBoxLayout()
        self.statusLinesGroup.setLayout(self.statusLinesLayout)
        self.statusLineLengthSlider = NoKeyHorizontalSlider(Qt.Horizontal)
        self.statusLineLengthSlider.setMinimum(0)
        self.statusLineLengthSlider.setMaximum(100)
        self.statusLineLengthSlider.setSingleStep(1)
        self.statusLineLengthSlider.setValue(75)
        self.statusLineLengthSlider.valueChanged.connect(self.changeLineLength)
        self.statusLinesLayout.addWidget(self.statusLineLengthSlider)
        self.statusLineLengthValue = QLabel("75")
        self.statusLinesLayout.addWidget(self.statusLineLengthValue)
        self.statusLayout.addWidget(self.statusLinesGroup)
        
        # Abstandhalter
        self.statusLayout.addStretch(1)
        
        # Speichern
        self.statusSpeichernButton = QPushButton("Speichern")
        self.statusSpeichernButton.clicked.connect(self.m.save)
        self.statusLayout.addWidget(self.statusSpeichernButton)
        
        # Restart
        self.statusRestartButton = QPushButton("Neustart")
        self.statusRestartButton.clicked.connect(self.restart)
        self.statusLayout.addWidget(self.statusRestartButton)
        

    def restart(self):
        self.m.restart()
        self.weltView.setMaximumLineLength(self.statusLineLengthSlider.value())


    def changeLineLength(self, value):
        self.statusLineLengthValue.setText(str(value))
        self.weltView.setMaximumLineLength(value)

        
    def getTracks(self):
        dir_path = "tracks"
        return [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]


    def getGhosts(self):
        dir_path = "tracks/" + self.m.trackName
        return [name.split(".")[0] for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]
    
        
    def changeGhost(self, ghost):
        self.m.changeGhost(ghost)
    
        
    def changeTrack(self, trackName):
        self.m.changeTrack(trackName)
        self.weltView.setMaximumLineLength(self.statusLineLengthSlider.value())
        
        
    def updateView (self):
        self.weltView.update_graphicsView()
        self.statusRundenText.setText(str(len(self.m.getPlayer().moves) - 1))


        
class NoArrowComboBox(QComboBox):
    def keyPressEvent(self, event):
        return  # Ignore arrow keys


class NoKeyHorizontalSlider(QSlider):
    def keyPressEvent(self, event):
        return