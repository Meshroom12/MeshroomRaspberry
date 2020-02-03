#!/usr/bin/env python


import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (1024, 768)
t=str(time.clock())

camera.start_preview()

camera.capture("photo" + t + ".jpg")

camera.stop_preview()
camera.close()

