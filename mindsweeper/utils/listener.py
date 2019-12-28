from connection import Connection
import socket

class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = socket.socket()
        
    def __enter__(self):
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        
    def __exit__(self, exceptions, error, traceback):
        self.socket.close()
        
    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}', backlog={self.backlog}, reuseaddr={self.reuseaddr})"
        
    def start(self):
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        
    def stop(self):
        self.socket.close()
        
    def accept(self):
        conn, address = self.socket.accept()
        return Connection(conn)
