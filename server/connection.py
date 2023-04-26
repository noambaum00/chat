import socket

class connection:
    def __init__(self, conn):
        self.conn = conn
    
    def send(self, data):
        self.conn.send(data.encode())
    
    def recv(self):
        try:
            a = ''
            while(len(a) < 3):
                a= s.recv(1024).decode().replace('\r\n', '')
            return a
        except ConnectionResetError:
            stop_threads = True
