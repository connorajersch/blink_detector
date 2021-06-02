from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAction
import webbrowser

import detect_blinks

class MenuBar(QMainWindow):
    """
    Menu bar for additional config options
    """

    def __init__(self, disk_dir: str, main_window: QMainWindow):
        super(MenuBar, self).__init__()

        self.disk_dir = disk_dir
        self.main_window = main_window

        menubar = main_window.menuBar()

        # Items In Menu Bar
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        # set up items within menus
        showCameraAct = QAction('&Show Camera Feed', self, checkable=True)
        showCameraAct.triggered.connect(self.toggleCameraFeed)
        showCameraAct.setChecked(True)
        fileMenu.addAction(showCameraAct)

        readMeAct = QAction('&View README', self)
        readMeAct.triggered.connect(self.openReadMe)
        helpMenu.addAction(readMeAct)

    """
    Action Functions
    """
    def openReadMe(self):
        webbrowser.open('https://github.com/connorajersch/blink_detector/blob/main/README.md')

    def toggleCameraFeed(self, state):

        if state:
            detect_blinks.showCamera = True
        else:
            detect_blinks.showCamera = False
