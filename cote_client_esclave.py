#!/usr/bin/env python

import io
import socket
import struct
import time
import picamera
import RPi.GPIO as GPIO
i=0


GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)                   # broche 12 est une sortie numerique
GPIO.setup(13, GPIO.OUT)                   # broche 13 est une sortie numerique

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('Paul-Legion', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    start = time.time()
    stream = io.BytesIO()
    
    time.sleep(5)
    
    
    if(GPIO.input(12)==1)
        GPIO.output(13, GPIO.HIGH)
        camera.capture(stream, 'jpeg')
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        # If we've been capturing for more than 30 seconds, quit
        #if time.time() - start > 30:
         #   break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    end
        
finally:
    connection.close()
    client_socket.close()
