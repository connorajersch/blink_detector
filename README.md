## HMSLab: Blink Detection Data Collector
By: Connor Ajersch and Mathew Dunne

### Overview
This repository provides a data collection tool which can be used to track blinking through the use of a Webcam. This program has functionality for storing and uploading locally collected data to Dropbox through the use of the Dropbox API. PyQt5 was used for the GUI, opencv and dlib were used for the webcam facial landmark tracking.

#### Setup (Only if you plan on building your own version of the program!)
If python is not yet installed on your computer, you can download it from [here](https://www.python.org/downloads/).  Ensure that in the setup, python is added to your path variables.  This can be checked using the following command:

 ```
python -V
```

You will also have to download this repository to your computer, which can be done using git.  If git is not installed on your computer, you can download it from [here](https://git-scm.com/download/win).  To make sure that git is installed on your computer and run the following command:

```
git --version
```

After you have verified that both python and git are installed on your computer, run the following command to install the Eye Tracking Data Collection software.

```
git clone https://github.com/Human-Systems-Lab/Eye-Tracking-Data-Collection.git
cd Eye-Tracking-Data-Collection
pip install -r requirements.txt
```

Naviagte to [the Dropbox Developer site](https://www.dropbox.com/developers) to make an "app" through which an API key will be obtained. Once you have the API key, you need to enter it into the main.py file where you see the code `dbx = dropbox.Dropbox('PASTE_API_KEY_HERE')`.

Now the program can be ran using python by running the following command:
```
python main.py
```

To build the enitre program (including all dependancies) into a single execuable file, run the following command in the Python terminal.

```
pyinstaller main.py --name="Eye Tracking Data Collector" --icon="assets/hslab_logo.ico" --noconsole --onefile
```

This command requires the pyinstaller module, which can be installed using:

```
pip install pyinstaller
```

Runnning pyinstaller with these parameters will output a single exe file to the /dist folder within the project directory.

#### Running The Program
Run the .exe file that you built or were provided. Click the green "Start Data Collection" button. A window showing the webcam feed should open, which includes text detailing the blink count. You can minimize this window if you prefer. Once you are ready to stop the data collection, click the red "Stop Data Collection" button. At this point, the collected data will be automatically uploaded to the linked dropbox. 
