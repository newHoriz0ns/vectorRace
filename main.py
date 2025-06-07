import sys

from PyQt5.QtGui import QSurfaceFormat 
from PyQt5.QtWidgets import QApplication

import mainFrame.mainFrame as mf
import mainFrame.vrVLM as vlm

# Replace in own App
import vrModel


import saveRouteToFile


CONTINOUS_UPDATE = True


if __name__ == "__main__":
    print ("Starte Anwendung ....")

    app = QApplication(sys.argv)


    format = QSurfaceFormat()
    format.setDepthBufferSize(24)
    format.setStencilBufferSize(8)
    format.setVersion(3, 2)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format)



    ###########
    # INIT MODEL HERE
    m = vrModel.VectorRaceModel(trackName="Apri")
    vrVlm = vlm.VectorRaceVLM(m)

    ###########

    # Init MainFrame
    window = mf.MainFrame(m)
 
    # Setze Controller in View
    window.set_viewLayerManager(vrVlm)
    
    # Setze View in Controller 
    vrVlm.set_viewContainer(window.view)

    # Setze View in Model (notify)
    m.setView(vrVlm)

    # StartUp Finished -> Start UpdateTimer
    if(CONTINOUS_UPDATE):
        window.init_updateRoutine()
        window.start_updateRoutine()

    window.showMaximized()

    app.exec()


    # TODO: Icon
    # TODO: Icon in Taskleiste
    # TODO: Single Open
    # TODO: Crash abfangen