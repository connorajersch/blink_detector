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
from MenuBar import MenuBar
import dropbox


disk_dir = ""

'''
Code to compile to exe/pkg:
pyinstaller main.py --name="Blink Tracking Data Collector" --icon="assets/hslab_logo.ico" --noconsole --onefile --hidden-import scipy.spatial.transform._rotation_groups --add-data "shape_predictor_68_face_landmarks.dat";.
'''

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setCursor(Qt.ArrowCursor)

        self.setWindowIcon(QtGui.QIcon(resource_path("assets/HSL-logo.png")))
        self.setWindowTitle("HSL | Blink Detection Data Collection")
        self.setGeometry(500, 300, 500, 300) #x,y,width,height

        # main widget
        self.main_ui_widget = MainWidget(disk_dir)
        main_widget = QDockWidget("", self)
        main_widget.setWidget(self.main_ui_widget)
        main_widget.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, main_widget)

        # menu bar
        self.menu_bar = MenuBar(disk_dir, self)

    def shutdown(self):
        self.main_ui_widget.shutdown()


# used to include the icon in the pyinstall build
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def main():
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
