import time

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import detect_blinks

class MainWidget(QWidget):

    isCollectingData = False
    defaultThreshold = 0.27

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


        #slider to set threshold
        threshold_slider_layout = QHBoxLayout()
        threshold_slider_layout.setAlignment(Qt.AlignHCenter)
        self.thresholdSlider = QSlider(Qt.Horizontal, self)
        self.thresholdSlider.setRange(0,100)
        self.thresholdSlider.setFocusPolicy(Qt.NoFocus)
        self.thresholdSlider.setPageStep(10)
        self.thresholdSlider.setSingleStep(1)
        self.thresholdSlider.setValue(50)

        #label of threshold value
        self.thresholdLabel = QLabel(str(self.defaultThreshold), self)
        self.thresholdLabel.setAlignment(Qt.AlignHCenter)
        self.thresholdLabel.setMaximumWidth(80)

        #other label
        self.sliderTitleLabel = QLabel("Threshold Value for Blink Detection (Default = " + str(self.defaultThreshold) + "):")

        threshold_slider_layout.addWidget(self.thresholdSlider)
        threshold_slider_layout.addSpacing(15)
        threshold_slider_layout.addWidget(self.thresholdLabel)

        threshold_slider_widget = QWidget()
        threshold_slider_widget.setLayout(threshold_slider_layout)

        vertical_slider_layout = QVBoxLayout()
        vertical_slider_layout.addWidget(self.sliderTitleLabel)
        vertical_slider_layout.addWidget(threshold_slider_widget)
        vertical_slider_widget = QWidget()
        vertical_slider_widget.setLayout(vertical_slider_layout)

        layout = QVBoxLayout()
        layout.addWidget(main_button_widget)
        layout.addWidget(vertical_slider_widget)

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
        self.thresholdSlider.valueChanged.connect(self.sliderValueChanged)

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

    def sliderValueChanged(self, value):

        #convert value from int (0-100) to float
        realValue = (0.27/50)*value

        self.thresholdLabel.setText(str(realValue.__round__(2)))