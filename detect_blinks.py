# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import platform
import ctypes
import sys
import os
import dlib
import cv2
import time
import datetime
import dropbox
import csv
from dropbox_serializer import DropboxSerializer
import threading

dbx = dropbox.Dropbox("nKFNWY-52lMAAAAAAAAAAcy6naEI8jJEaTGvn4BADZPmiWGdEbGoBBYXqvQ9--4T")

global disk_dir
global thresh_disk_dir
plat = platform.system()
if plat == "Windows":
    disk_dir = os.path.join(os.getenv("APPDATA"), "HSL")
    thresh_disk_dir = disk_dir

elif plat == "Linux":
    disk_dir = os.path.join(os.path.expanduser("~"), ".HSL")
    thresh_disk_dir = disk_dir

elif plat == "Darwin":
    disk_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), "HSL")
    thresh_disk_dir = disk_dir

disk_dir = os.path.join(disk_dir, "Blink Detector Data")


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


# needed to work as a single exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


databasePath = resource_path('shape_predictor_68_face_landmarks.dat')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", default=databasePath,
                help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="camera",
                help="path to input video file")
ap.add_argument("-t", "--threshold", type=float, default=0.27,
                help="threshold to determine closed eyes")
ap.add_argument("-f", "--frames", type=int, default=2,
                help="the number of consecutive frames the eye must be below the threshold")

status = "Data collection is not currently running."
stopButtonPressed = False
showCamera = True


def main():
    with open(os.path.join(thresh_disk_dir, "threshold.txt"), "r") as f:
        threshold = float(f.read())
        print("Set the threshold parameter to: " + str(threshold))
        f.close()
    global status
    global stopButtonPressed
    args = vars(ap.parse_args())
    EYE_AR_THRESH = threshold
    EYE_AR_CONSEC_FRAMES = args['frames']

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    start_time = time.time()

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    status = "Loading facial landmark predictor..."
    print(status)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    status = "Starting video stream thread..."
    print(status)
    if args['video'] == "camera":
        vs = VideoStream(src=0).start()
        fileStream = False
    else:
        vs = FileVideoStream(args["video"]).start()
        fileStream = True

    time.sleep(1.0)
    temp = []
    ear_temp = []
    status = "Data Collection Running!"
    print(status)

    # loop over frames from the video stream
    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        if fileStream and not vs.more():
            break

        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1

                    temp_time = time.time() - start_time
                    temp.append(temp_time)
                    ear_temp.append(ear)

                # reset the eye frame counter
                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if showCamera:
            # show the frame
            cv2.imshow("Frame", frame)
            # print("eye thresh = " + str(EYE_AR_THRESH))
            key = cv2.waitKey(1) & 0xFF

        if stopButtonPressed:
            break

    # end of while loop

    end_time = time.time()
    print(TOTAL)
    print('time cost', end_time - start_time, 's')
    print(temp)
    currentDateTime = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
    with open(os.path.join(disk_dir, str(currentDateTime) + '.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(temp)
        spamwriter.writerow(ear_temp)
    DropboxSerializer(dbx).upload_file(os.path.join(disk_dir, str(currentDateTime) + '.csv'),
                                       '/Collected Data/' + str(currentDateTime) + '.csv')
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    status = "Data Collection Stopped."
    print(status)


class MultiThreadBlinkDetector(object):
    """
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self):
        """ Constructor """
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        '''Function that runs in background'''
        main()
