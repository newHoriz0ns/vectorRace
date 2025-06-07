
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsScene, QLineEdit
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
        
        # Name
        self.statusNameGroup = QGroupBox("Spieler")
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
        
        # Abstandhalter
        self.statusLayout.addStretch(1)
        
        # Speichern
        self.statusSpeichernButton = QPushButton("Speichern")
        self.statusSpeichernButton.clicked.connect(self.m.save)
        self.statusLayout.addWidget(self.statusSpeichernButton)
        
        # Restart
        self.statusRestartButton = QPushButton("Neustart")
        self.statusRestartButton.clicked.connect(self.m.restart)
        self.statusLayout.addWidget(self.statusRestartButton)
        
        
    def updateView (self):
        self.weltView.update_graphicsView()
        self.statusRundenText.setText(str(len(self.m.getPlayer().moves) - 1))