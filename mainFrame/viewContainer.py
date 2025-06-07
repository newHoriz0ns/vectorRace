"""
author: Paul Benz
lastChange: 31.07.23
version: v0.2

Concept:
* Layout von QWidget und dessen Organisation
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout

class ViewContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.viewStructure = {}
        self.currentView = None


    def add_view(self, viewID, view):
        self.viewStructure[viewID]  = view
        self.mainLayout.addWidget(view)


    def set_currentView(self, viewID):
        for v in self.viewStructure:
            self.viewStructure[v].setVisible(v == viewID)