import socket
import ssl

class connection:
    def __init__(self, sock):
        self.sock = sock

    
    def send(self, data):
        self.sock.send(data.encode())
    
    def recv(self):
        try:
            a = ''
            while(len(a) < 3):
                a= self.sock.recv(1024).decode().replace('\r\n', '')
            return a
        except ConnectionResetError:
             self.close()

    def close(self):
        self.sock.close()


class SSLConnection:
    def __init__(self, sock):
        self.sock = sock
        self.ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="HIGH")
        
    def send(self, data):
        return self.ssl_sock.send(data)
        
    def recv(self):
        return self.ssl_sock.recv()
        
    def close(self):
        self.ssl_sock.close()
        self.sock.close()

