#!/usr/bin/env python

import io
import socket
import struct
import time
import picamera
i=0

etat = True

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('Paul-Legion', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wrb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    start = time.time()
    stream = io.BytesIO()
    
    time.sleep(1)   
    
    while etat:   

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        msg = client_socket.recv(1024)
        print(msg)
        
        if msg=='photo':
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
        if msg=='stop':
            etat=False
            
            
    # Reset the stream for the next capture
    stream.seek(0)
    stream.truncate()        
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0x00000000))
    print("fin d'envoi");
        
finally:
    connection.close()
    client_socket.close()
