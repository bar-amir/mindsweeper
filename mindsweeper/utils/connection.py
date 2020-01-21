import socket

class Connection:
    def __init__(self, socket):
        pass
    
    def connect(host, port):
    """"""
        pass
    
    def send_message(self, data):
    """"""
        pass
    
    def receive_message():
    """"""
        pass

class Connection:
    def __init__(self, socket):
        self.socket = socket
        
    def __enter__(self):
        return self
        
    def __exit__(self, exception, error, traceback):
        self.socket.close()
        
    def __repr__(self):
        sn = self.socket.getsockname()
        pn = self.socket.getpeername()
        return f"<Connection from {sn[0]}:{sn[1]} to {pn[0]}:{pn[1]}>"
    
    def send(self, data):
        self.socket.sendall(data)
        
    def receive(self, size):
        data = b''
        while len(data) < size:
            m = self.socket.recv(size)
            if not m:
                break;
            data += m
        if not len(data) == size:
            raise Exception('Error')
        return data
    
    def connect(host, port):
        soc = socket.socket()
        soc.connect((host, port))
        return Connection(soc)
    
