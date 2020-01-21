import socket
import time
import datetime    
import struct 
import threading
import pathlib

from .cli import CommandLineInterface

cli = CommandLineInterface()

def run_server(address, data_dir):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen()
    
    p = pathlib.Path(data_dir)

    while True:
        connection, address = server.accept()
        handler = Handler(connection, p)
        handler.start()

class Handler(threading.Thread):
    def __init__(self, connection, p):
        super().__init__()
        self.connection = connection
        self.p = p
        self.lock = threading.Lock()
    def run(self):
        signature = b''
        while len(signature) < 20:
            msg = self.connection.recv(20)
            if not msg:
                break
            signature += msg
        
        if len(signature) == 20:
            user_id, ts, t_len = struct.unpack('<QQI', signature)
        else:
            raise Exception('Error')
        
        if (t_len > 0):
            t = b''
            while len(t) < t_len:
                msg = self.connection.recv(t_len)
                if not msg:
                    break
                t += msg
            t = struct.unpack('<%ds' % (t_len,), t)[0].decode()
        else:
            raise Exception('Error')
        if (t_len != len(t)):
            raise Exception('Error')
        
        dt = datetime.datetime.fromtimestamp(ts)
        dir_path = self.p/str(user_id)
        pathlib.Path(dir_path).mkdir(exist_ok=True)
        file_name = dt.strftime('%Y-%m-%d_%H-%M-%S')+'.txt'
        file_path = dir_path/file_name
        self.lock.acquire()
        try:
            lb = ''
            if pathlib.Path.exists(file_path):
                lb = '\n'
            with open(file_path, 'a') as fid:
                fid.write(lb + t)
                fid.close()
            print(file_path)
        finally:
            self.lock.release()

def run(address, data):
    try:
        address = address.split(":")
        address[1] = int(address[1])
        address = tuple(address)
        run_server(address, data)
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
