import socket
import sys
import os
import subprocess

def print_screen(conn):
    conn.send("\x1b[2J\x1b[H" + "\033[94m") # clear terminal & colored blue
    conn.sendall(" /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$\n" +
                " | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/\n" + 
                " | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ \n" +
                " | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  \n" +
                " | $$__  $$| $$__  $$| $$  $$$$| $$  $$  \n" +
                " | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ \n" +
                " | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$\n" +
                " |_______/ |__/  |__/|__/  \__/|__/  \__/\n\n")

    conn.send("\033[1m" + "\033[95m") # colored pink and bold
    conn.sendall(" =========================================\n" +
                 " Hello, customer. \n What would you like to do?\n\n" +
                 " 1. Login \n" +
                 " 2. Register \n" +
                 " =========================================\n")
    conn.send('\033[0m') # colored white(normal)

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
            # print main screen
            print_screen(connection) 
            
        finally:
            # Close the connection
            connection.close()
            print("closed")

if __name__ == "__main__":
    server()
