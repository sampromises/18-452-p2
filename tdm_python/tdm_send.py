import time
import socket
import sys

# Constants
HOST = '127.0.0.1' # Localhost by default for debugging
PORT = 15232 # Debug port

#TDM_ON = False # If false, will not wait for any time
TDM_ON = True # If false, will not wait for any time
CHUNK_SIZE = 1024

# Globals
skt = None

# Connect to a TCP socket, host is a string, port is an int
def connect():
    global skt
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((HOST, PORT))
    print('Successfully connected to {}:{}'.format(HOST, PORT))

def send():
    sent_bytes = 0
    total_bytes = CHUNK_SIZE*10

    if (TDM_ON):
        while (sent_bytes < total_bytes):
            skt.sendall(b'A'*CHUNK_SIZE)
            sent_bytes += CHUNK_SIZE
            print('Sent {} bytes...'.format(CHUNK_SIZE))
    else:
        skt.sendall(b'A'*total_bytes)
        print('Sent {} bytes...'.format(total_bytes))



def main():
    connect()
    send()
    skt.close()


if __name__ == '__main__':
    # If host, port were provided, otherwise use defaults
    if len(sys.argv) > 3:
        HOST = sys.argv[1]
        PORT = sys.argv[2]

    main()
