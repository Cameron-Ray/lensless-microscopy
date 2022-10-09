from time import sleep

from picamera import PiCamera

camera = yYPiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()
