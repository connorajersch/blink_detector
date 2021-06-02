import time
import os
import platform

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import detect_blinks

# sets up folder to store local data in based on the user's OS
# might not need to be done here because it's done in main also
global disk_dir
plat = platform.system()
if plat == "Windows":
    disk_dir = os.path.join(os.getenv("APPDATA"), "HSL")

elif plat == "Linux":
    disk_dir = os.path.join(os.path.expanduser("~"), ".HSL")

elif plat == "Darwin":
    disk_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), "HSL")


# code to set up the main window that the user interacts with
class MainWidget(QWidget):
    isCollectingData = False  # gets set to true when data collection starts
    defaultThreshold = 0.27  # default threshold value for detecting a blink

    def __init__(self, disk_dir: str):
        super(MainWidget, self).__init__()

        self.disk_dir = disk_dir

        start_stop_button_layout = QVBoxLayout()  # create a vertical (V) layout to display button and text underneath
        start_stop_button_layout.setAlignment(Qt.AlignHCenter)  # horizontally center items within the layout

        # create button that starts/stops data collection
        self.start_stop_button = QPushButton("Start Data Collection")
        self.start_stop_button.setFont(QFont('Arial', 18))
        self.start_stop_button.setStyleSheet("background-color: #8deb9c")
        self.start_stop_button.setMaximumWidth(600)
        self.start_stop_button.setMaximumHeight(120)
        self.start_stop_button.setMinimumWidth(300)
        self.start_stop_button.setMinimumHeight(100)

        # create line of text under button that displays status of data collection
        self.status_label = QLabel("Data collection is not currently running.")
        self.status_label.setAlignment(Qt.AlignHCenter)
        self.status_label.setFont(QFont('Arial', 14))

        # add the button and text widgets above to the vertical layout with spacing in between
        start_stop_button_layout.addWidget(self.start_stop_button)
        start_stop_button_layout.addSpacing(20)
        start_stop_button_layout.addWidget(self.status_label)

        #  create a new widget that contains the layout that contains the button and text
        main_button_widget = QWidget()
        main_button_widget.setLayout(start_stop_button_layout)

        # create a horizontal (H) layout to display the slider and a label beside it
        threshold_slider_layout = QHBoxLayout()
        threshold_slider_layout.setAlignment(Qt.AlignHCenter)  # horizontally center items within the layout

        # slider to set threshold
        self.thresholdSlider = QSlider(Qt.Horizontal, self)
        self.thresholdSlider.setRange(0, 100)
        self.thresholdSlider.setFocusPolicy(Qt.NoFocus)
        self.thresholdSlider.setPageStep(10)
        self.thresholdSlider.setSingleStep(1)
        self.thresholdSlider.setValue(50)  # starting value

        # label of threshold value
        self.thresholdLabel = QLabel(str(self.defaultThreshold), self)
        self.thresholdLabel.setAlignment(Qt.AlignHCenter)
        self.thresholdLabel.setMaximumWidth(80)

        # other label that displays description of slider
        self.sliderTitleLabel = QLabel(
            "Threshold Value for Blink Detection (Default = " + str(self.defaultThreshold) + "):")

        # add the slider and label to the horizontal layout with spacing in between
        threshold_slider_layout.addWidget(self.thresholdSlider)
        threshold_slider_layout.addSpacing(15)
        threshold_slider_layout.addWidget(self.thresholdLabel)

        #  create a new widget that contains the layout that contains the slider and label
        threshold_slider_widget = QWidget()
        threshold_slider_widget.setLayout(threshold_slider_layout)

        # create a vertical layout that contains the description label and slider/label combo widget
        vertical_slider_layout = QVBoxLayout()
        vertical_slider_layout.addWidget(self.sliderTitleLabel)
        vertical_slider_layout.addWidget(threshold_slider_widget)

        # create a new widget that contains the vertical layout for the description and slider
        vertical_slider_widget = QWidget()
        vertical_slider_widget.setLayout(vertical_slider_layout)

        # create a final layout that contains the button widget and slider widget
        layout = QVBoxLayout()
        layout.addWidget(main_button_widget)
        layout.addWidget(vertical_slider_widget)

        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.set_connections()

    def shutdown(self):  # called when window closes
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

        if self.isCollectingData:  # if the button is pressed while collection is running, stop collection
            detect_blinks.stopButtonPressed = True
            self.status_label.setText("Data Collection Stopped.")
            self.start_stop_button.setText("Start Data Collection")
            self.start_stop_button.setStyleSheet("background-color: #8deb9c")  # set colour to red
            self.isCollectingData = False

        else:  # if the button is pressed while collection is NOT running, start collection
            detect_blinks.stopButtonPressed = False
            detect_blinks.MultiThreadBlinkDetector()  # start data collection function
            self.status_label.setText("Data Collection Started!")
            self.start_stop_button.setText("Stop Data Collection")
            self.start_stop_button.setStyleSheet("background-color: #f58997")  # set colour to green
            time.sleep(3)
            self.isCollectingData = True

    # called when the slider value is changed
    def sliderValueChanged(self, value):

        # convert value from int (0-100) to float with 50 becoming 0.27 (default value)
        realValue = (self.defaultThreshold / 50) * value

        # update label with rounded decimal value
        self.thresholdLabel.setText(str(realValue.__round__(2)))

        # write new threshold value to a file to read later
        with open(os.path.join(disk_dir, "threshold.txt"), "w") as f:
            f.write(str(realValue.__round__(2)))
            # print("writing real value: " + str(realValue.__round__(2)))
            f.close()
