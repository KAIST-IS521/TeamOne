import socket, sys
from const import *

def print_logo(conn):
    conn.send(CLEAR_TERMINAL + COR_LOGO) # clear terminal & colored
    conn.sendall("  /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$\n" +
                 " | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/\n" + 
                 " | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ \n" +
                 " | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  \n" +
                 " | $$__  $$| $$__  $$| $$  $$$$| $$  $$  \n" +
                 " | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ \n" +
                 " | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$\n" +
                 " |_______/ |__/  |__/|__/  \__/|__/  \__/\n\n")

    conn.send(COR_BASE) # colored
    conn.send(" =========================================\n")

def get_option(conn):
    while True:
        # print main screen
        print_logo(conn)
        conn.sendall(" Hello, customer. \n" +
                     " 1. Login \n" +
                     " 2. Register \n\n") 
     
        conn.send(" What would you like to do? -> ")
    
        # get an option from user

def server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 1588)
    print >> sys.stderr, 'starting up on %s port %s' %server_address
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(1)
    
    while True:
        connection, client_address = sock.accept()

        try:
            get_option(connection)
        finally:
            # Close the connection
            connection.send(COR_DEFAULT) # colored white(normal)
            connection.close()
            print("closed")

if __name__ == "__main__":
    server()
