
from PyQt5.QtWidgets import QGraphicsView, QOpenGLWidget
from PyQt5.QtGui import QSurfaceFormat

import time

from weltGraphicsScene import WeltGraphicsScene

class WeltGraphicsViewWidget(QGraphicsView):

    def __init__(self, m) -> None:
        super().__init__()

        # GraphicsScene
        self.wgs = WeltGraphicsScene(m)
        self.setScene(self.wgs)

        #self.setFixedSize(1000, 600)

        # OPEN GL Widget
        self.oglw = QOpenGLWidget()
        
        sf = QSurfaceFormat()
        sf.setSamples(1)
        sf.setSwapInterval(1)
        self.oglw.setFormat(sf)
        self.setViewport(self.oglw)

        # self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setViewportUpdateMode(1)

        # self.centerOn(self.wgs.centerItem())

        self.lastUpdate = 0



    def update_graphicsView(self):  
        self.wgs.update_graphicsScene()
        # self.centerOn(self.wgs.centerItem())

        # Update GL
        self.oglw.update