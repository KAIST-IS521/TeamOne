import socket, sys, re, json

def saveflag():
    print("saveflag")

def server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 42)
    print >> sys.stderr, 'starting up on %s port %s' %server_address
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(1)
    
    while True:
        connection, client_address = sock.accept()

        try:
            data = []
            while True:
                byte = connection.recv(1)
                if byte == '':
                    break
                data.append(byte)
            saveflag(''.join(data))
        finally:
            # Close the connection
            connection.close()
            print("closed")

if __name__ == "__main__":
    server()
