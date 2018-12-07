import socket

# TCP sockets
host = '127.0.0.1'
port = 8080
skt = None

def main():
    global skt
    try:
        ckt.bind((host,port))
    except socket.error:
        print("Socket binding failed for %s with port number %d\n", host, port)

    skt.listen()
    (conn, addr) = skt.accept()
    print("connected!")

    while True:
        nodes = {b'2': 0, b'3': 0, b'4': 0}
        packet = bytearray()
        while length(nodes) != 0:
            data = conn.recv(chunksize)
            if data[0] in nodes:
                packet.extend(data[1:])
                del nodes[data[0]]
        skt.sendall(packet)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Command line argument parser") 
    parser.add_argument('--host', type=str, help='Required host ip address')
    parser.add_argument('--port', type=int, help='Required port number')
    parser.add_argument('--file', type=str, help='Required cvs file')
    args = parser.parse_args()

    # set optional host/port if provided
    if (args.host != None):
        host = args.host
    if (args.port != None):
	port = args.port
    main()
