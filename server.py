from PIL import Image
import socket
import sys
import struct

BYTES_IN_IMAGE = 12288000

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a port
# server_address = ('localhost', 6666)
server_address = ('192.168.2.249', 6666)
print('Starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

def recv_exact(conn, length):
    buffer = b''
    while len(buffer) < length:
        data = conn.recv(length - len(buffer))
        if not data:
            return data
        buffer += data
    return buffer

while True:
    # Wait for connection
    print('Waiting for connection')
    connection, client_address = sock.accept()

    try:
        print('Connection from ', client_address)
        
        # Receieve the data in small chunks and retransmit it
        while True:
            image_bytes = recv_exact(connection, BYTES_IN_IMAGE)
            if (len(image_bytes) > 0):
                print(len(image_bytes))
                image = Image.frombytes('RGB', (2560, 1600), image_bytes, 'raw')
                image.show()
                    
    finally:
        # Clean up connection
        print('Clean up connection')
        connection.close()
