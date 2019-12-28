from cli import CommandLineInterface

cli = CommandLineInterface()

def upload_thought(address, user_id, thought):
    import socket
    import time
    import struct
    
    conn = socket.socket()
    conn.connect(address)
    ts = int(time.time())
    t = thought.encode()
    msg = struct.pack("<QQI%ds" % (len(t),),user_id,ts,len(t),t)
    conn.sendall(msg)
    
@cli.command
def upload(address, user, thought):
    try:
        address = address.split(":")
        address[1] = int(address[1])
        address = tuple(address)
        upload_thought(address, int(user), thought)
        print('done')

    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    cli.main()
