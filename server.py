from PIL import Image
import socket
import sys
import struct
import time
import pygame

BYTES_IN_IMAGE = 12288000
#BYTES_IN_IMAGE = 16384000
#BYTES_IN_IMAGE = 32768000

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a port
# server_address = ('localhost', 6666)
server_address = ('192.168.2.249', 7000)
print('Starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

pygame.init()
w = 2560
h = 1600
size=(w,h)
screen = pygame.display.set_mode(size)
c = pygame.time.Clock()

cur_time = time.time()

def recv_exact(conn, length):
    buffer = b''
    while len(buffer) < length:
        data = conn.recv(length - len(buffer))
        if not data:
            return data
        buffer += data
        #if (len(data) > 0):
        #    print(len(buffer))
    return buffer

def convert_to_16_bit(byte_array):
    converted_array = []
    for idx in range(len(byte_array) // 2):
        if not byte_array[2*idx] == 0 and not byte_array[2*idx + 1] == 0:
            print("%d %d", byte_array[2*idx], byte_array[2*idx + 1])
        converted_array.append(byte_array[2*idx] << 4 + byte_array[2*(idx)+1])
    return converted_array

import pdb; pdb.set_trace()

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
                #print(len(image_bytes))
                img = pygame.image.fromstring(image_bytes, size, 'RGB')
                screen.blit(img,(0,0))
                pygame.display.update()
                pygame.event.poll()
                #image = Image.frombytes('RGB', (2560, 1600), image_bytes, 'raw')
                # print(time.time())
                #image.show()
                now_time = time.time()
                print('from last time took %d ms' % (now_time - cur_time))
                cur_time = now_time
                    
    finally:
        # Clean up connection
        print('Clean up connection')
        connection.close()
