import socket
import ssl

class connection:
    def __init__(self, conn):
        self.conn = conn

    
    def send(self, data):
        self.conn.send(data.encode())
    
    def recv(self):
        try:
            a = ''
            while(len(a) < 3):
                a= self.conn.recv(1024).decode().replace('\r\n', '')
            return a
        except ConnectionResetError:
            stop_threads = True

    def close(self):
        self.conn.close()


class SSLConnection:
    def __init__(self, sock):
        self.sock = sock
        self.ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="HIGH")
        
    def send(self, data):
        return self.ssl_sock.send(data)
        
    def recv(self, bufsize):
        return self.ssl_sock.recv(bufsize)
        
    def close(self):
        self.ssl_sock.close()
        self.sock.close()

