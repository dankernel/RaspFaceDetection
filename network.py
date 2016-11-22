import socket
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from time import sleep
import cv2

# File
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/opencv/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')

with picamera.PiCamera() as camera:
  camera.resolution = (480, 320)
  camera.framerate = 24

  server_socket = socket.socket()
  server_socket.bind(('0.0.0.0', 8002))
  server_socket.listen(0)

  camera.annotate_text = 'dkdk'

  # Accept a single connection and make a file-like object out of it
  connection = server_socket.accept()[0].makefile('wb')

  print "11"

  try:
    camera.start_recording(connection, format='h264')
    rawCapture = PiRGBArray(camera, size=(480, 320))

    print "22"

    # Add..
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      image = frame.array

      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(50, 50),
        flags = cv2.CASCADE_SCALE_IMAGE
      )

      for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        s = ""
        s += str(x)
        s += " / "
        s += str(y)

        if x < 150:
          s += "<<"

        if 330 < x:
          s += ">>"

        camera.annotate_text = s 

      # clear the stream in preparation for the next frame
      rawCapture.truncate(0)

      # Q Key
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
        break

    # ...?
    camera.wait_recording(10)
    camera.stop_recording()
  finally:
    connection.close()
    server_socket.close()
