from PIL import Image
import socket
import sys
import time

BYTES_IN_IMAGE = 12288000

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.2.249', 7000)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    #while True:
    im = Image.open('./cyrus_real.png')
    im_bytes = im.tobytes()
    print(time.time())
    
    sock.sendall(im_bytes)

finally: 
    print('Closing socket')
    sock.close()
