# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Profile
import cProfile
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(480, 320))
 
# allow the camera to warmup
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/opencv/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
 
def extract_features(image):
   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(50, 50),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # iterate over all identified faces and try to find eyes
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Image', image)

def mainfunc():
  # capture frames from the camera
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	  # grab the raw NumPy array representing the image, then initialize the timestamp
	  # and occupied/unoccupied text
    image = frame.array
 
    # show the frame & OpenCV
    extract_features(image)
 
	  # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Q Key
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cProfile.run('mainfunc()') 
