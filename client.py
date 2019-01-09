from PIL import Image
import socket
import sys

BYTES_IN_IMAGE = 1228800

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6666)
print('Connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    #while True:
    im = Image.open('./wow_img.jpeg')
    im_bytes = im.tobytes()
    
    sock.sendall(im_bytes)

finally: 
    print('Closing socket')
    sock.close()