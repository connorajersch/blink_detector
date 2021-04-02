import os
import time
import threading

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFontDialog

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import detect_blinks

class MainWidget(QWidget):
    """
    Widget for admin related tasks
    """
    isCollectingData = False

    def __init__(self, disk_dir: str):
        super(MainWidget, self).__init__()

        self.disk_dir = disk_dir

        start_stop_button_layout = QVBoxLayout()
        start_stop_button_layout.setAlignment(Qt.AlignHCenter)
        self.start_stop_button = QPushButton("Start Data Collection")
        self.start_stop_button.setFont(QFont('Arial', 18))
        self.start_stop_button.setStyleSheet("background-color: #8deb9c")
        self.start_stop_button.setMaximumWidth(600)
        self.start_stop_button.setMaximumHeight(120)
        self.start_stop_button.setMinimumWidth(300)
        self.start_stop_button.setMinimumHeight(100)

        self.newline = QLabel("")

        self.status_label = QLabel("Data collection is not currently running.")
        self.status_label.setAlignment(Qt.AlignHCenter)
        self.status_label.setFont(QFont('Arial', 14))


        #main button to start or stop data collection
        start_stop_button_layout.addWidget(self.start_stop_button)
        start_stop_button_layout.addWidget(self.newline)
        start_stop_button_layout.addWidget(self.status_label)

        main_button_widget = QWidget()
        main_button_widget.setLayout(start_stop_button_layout)


        layout = QVBoxLayout()
        layout.addWidget(main_button_widget)

        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.set_connections()

    def shutdown(self):
        pass


    def set_connections(self):
        """
        Sets up all of the connections between the components of the Widget
        """
        self.start_stop_button.pressed.connect(self.toggleDataCollection)

    def toggleDataCollection(self):
        """
        Called when the start/stop collection button is pressed
        """

        if self.isCollectingData:
            detect_blinks.stopButtonPressed = True
            self.status_label.setText("Data Collection Stopped.")
            self.start_stop_button.setText("Start Data Collection")
            self.start_stop_button.setStyleSheet("background-color: #8deb9c")
            self.isCollectingData = False
        else:
            detect_blinks.stopButtonPressed = False
            detect_blinks.MultiThreadBlinkDetector()
            self.status_label.setText("Data Collection Started!")
            self.start_stop_button.setText("Stop Data Collection")
            self.start_stop_button.setStyleSheet("background-color: #f58997")
            time.sleep(3)
            self.isCollectingData = True
