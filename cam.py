#!/usr/bin/env python

#blablatest
import time
import picamera

camera = picamera.PiCamera()

camera.start_preview()

time.sleep(100)

camera.stop_preview()
camera.close()

#bbqjb