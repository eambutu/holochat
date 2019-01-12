from PIL import Image
import socket
import sys
import struct
import time
import pygame
from threading import Thread, Lock
import queue

#w = 500
#h = 200
w = 1200
h = 800
BYTES_IN_IMAGE = w * h * 3

class ListenThread(Thread):
    def __init__(self, obj, lock):
        Thread.__init__(self)
        self._obj = obj
        self._lock = lock
        self._terminating = False

    def destroy(self):
        self._terminating = True
        
    def recv_exact(self, conn, length):
        buffer = b''
        while len(buffer) < length:
            data = conn.recv(length - len(buffer))
            if not data:
                return data
            buffer += data
            #if (len(data) > 0):
            #    print(len(buffer))
        return buffer

    def run(self):
        # Create TCP/IP socket
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        # Bind socket to a port
        #server_address = ('localhost', 6666)
        server_address = ('192.168.1.67', 6000)
        #server_address = ('a0:ce:c8:0f:46:63', 6000)
        print('Starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        
        # Wait for connection
        print('Waiting for connection')
        connection, client_address = sock.accept()
        print('Connection from ', client_address)
        self._obj.connection_received()
        while True:
            try:
                image_bytes = self.recv_exact(connection, BYTES_IN_IMAGE)
                self._obj.post_new_data(image_bytes)
            finally:
                # Clean up connection
                print('Clean up connection')
                #connection.close()


def process_byte_string(byte_string):
    temp = bytearray(byte_string) 
    for idx in range(len(temp) // 3):
        temp[3*idx: 3*(idx + 1)] = byte_string[3*idx: 3*(idx + 1)][::-1]
    print('reversed image bytes')
    return bytes(temp)

class Runner(object):
    def __init__(self):
        self._lock = Lock()
        self._listener = ListenThread(self, self._lock)
        self._listener.start()
        self.image_queue = queue.Queue()
        self.has_connection = False

    def post_new_data(self, data):
        self.image_queue.put(data)

    def connection_received(self):
        self.has_connection = True

    def run(self):
        while not self.has_connection:
            time.sleep(0.01)
        pygame.init()
        size=(w,h)
        screen = pygame.display.set_mode(size)
        c = pygame.time.Clock()
        image_count = 1

        cur_time = time.time()
        first_time = True
       
        # Receieve the data in small chunks and retransmit it
        while True:
            while self.image_queue.empty():
                time.sleep(0.01)
            image_bytes = self.image_queue.get()
            if (len(image_bytes) > 0):
                print(len(image_bytes))
                print("Took %f seconds to receive" % (time.time() - cur_time))
                if first_time:
                    pygame.display.set_mode((0, 0), pygame.NOFRAME)
                    first_time = False
                img = pygame.image.fromstring(image_bytes, size, 'RGB')
                img = pygame.transform.flip(img, False, True)
                screen.blit(img,(0,0))
                pygame.display.update()
                pygame.event.poll()
                now_time = time.time()
                print('from last time took %f seconds' % (now_time - cur_time))
                cur_time = now_time
                        
        
if __name__=='__main__':
    runner = Runner()
    runner.run()
