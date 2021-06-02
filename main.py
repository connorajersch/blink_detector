# import the necessary packages
import os
import sys
import platform
import ctypes

from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDockWidget

from PyQt5.QtCore import Qt

from control_gui import MainWidget
from menu_bar import MenuBar
import dropbox

disk_dir = ""

'''
Code to compile to exe/pkg:
pyinstaller main.py --name="Blink Tracking Data Collector" --icon="assets/hslab_logo.ico" --noconsole --onefile --hidden-import scipy.spatial.transform._rotation_groups --add-data "shape_predictor_68_face_landmarks.dat";. --add-data "HSL-logo.png";.
'''


# create main window and add widget and menu bar to it
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setCursor(Qt.ArrowCursor)

        iconPath = resource_path("HSL-logo.png")
        self.setWindowIcon(QtGui.QIcon(iconPath))
        self.setWindowTitle("HSL | Blink Detection Data Collection")
        self.setGeometry(500, 300, 500, 300)  # x,y,width,height

        # main widget
        self.main_ui_widget = MainWidget(disk_dir)
        main_widget = QDockWidget("", self)
        main_widget.setWidget(self.main_ui_widget)
        main_widget.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, main_widget)

        # menu bar
        self.menu_bar = MenuBar(disk_dir, self)

    # runs when window is closed
    def shutdown(self):
        self.main_ui_widget.shutdown()


# needed to make icon work as a single exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    # sets up folder to store local data in based on the user's OS
    global disk_dir
    plat = platform.system()
    if plat == "Windows":
        disk_dir = os.path.join(os.getenv("APPDATA"), "HSL")
        my_app_id = u'HSL.BlinkDetection.DataCollector'  # arbitrary string
        # set taskbar icon to same as the window app icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    elif plat == "Linux":
        disk_dir = os.path.join(os.path.expanduser("~"), ".HSL")

    elif plat == "Darwin":
        disk_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), "HSL")

    else:
        print("Unsupported operating system: %s" % plat)
        print("This software only supports Windows, macOS, and Linux")
        exit(1)

    # opens/creates a file to store the threshold value (27 by default)
    with open(os.path.join(disk_dir, "threshold.txt"), "w") as f:
        f.write("0.27")
        f.close()

    if not os.path.isdir(disk_dir):
        os.mkdir(disk_dir)
    disk_dir = os.path.join(disk_dir, "Blink Detector Data")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    e_code = app.exec_()
    window.shutdown()
    sys.exit(e_code)


if __name__ == '__main__':
    main()
