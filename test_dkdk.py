from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.start_preview(fullscreen=False, window = (100, 100, 640, 480))
sleep(10)
