import socket, sys, re
from const import *
from util import *
from balance import *
from history import *
from transfer import *
from mypage import *

def get_username(conn):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(" [ Login ]\n" +
                     " Please input username and password. \n\n")

        if errmsg:
            conn.send(errmsg)

        conn.send(" * Username -> ")

        # get username from user
        data = recv_line(conn)

        # ID : lowerletter, upperletter, number
        regex = re.compile(REGEX_USERNAME)

        if data == '':
            errmsg = ERRMSG_USER_NULL
        elif regex.match(data) == None:
            errmsg = ERRMSG_USER_INVAL
        else:
            return data

def get_password(conn, name):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(" [ Login ]\n" +
                     " Please input username and password. \n\n" +
                     " * Username -> " + name + "\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(" * Password -> ")

        # get password from user
        data = recv_line(conn)
        
        if data == '':
            errmsg = ERRMSG_PW_NULL
        elif len(data) > LEN_PASSWORD:
            errmsg = ERRMSG_PW_LEN
        else:
            return data

def login(conn):

    # get & store username and password
    name = get_username(conn)
    pw = get_password(conn, name)

    # TODO SQL request and confirm

    # TODO add UI for login fail

    get_user_menu(conn, name)

def get_user_menu(conn, user):
    errmsg = ""

    while True:
        # print user menu
        print_logo(conn)
        conn.sendall(" [ User Menu ]\n" +
                     " Hello, " + user + ".\n\n" +
                     " 1. Check balance \n" + 
                     " 2. Check transaction history \n" +
                     " 3. Transfer \n" +
                     " 4. Edit user info & Remove account \n\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(" What would you like to do? -> ")
        
        # get an option from user
        data = recv_line(conn)

        if data == '1':
            user_check_balance(conn, user)
        elif data == '2':
            user_check_history(conn, user)
            break
        elif data == '3':
            user_transfer(conn, user)
        elif data == '4':
            user_mypage(conn, user)
            break
        else:
            errmsg = ERRMSG_OPTION

def get_main_menu(conn):
    errmsg = ""

    while True:
        # print main screen
        print_logo(conn)
        conn.sendall(" Hello, customer. \n" +
                     " 1. Login \n" +
                     " 2. Register \n\n") 
        if errmsg:
            conn.send(errmsg)

        conn.send(" What would you like to do? -> ")
    
        # get an option from user
	data = recv_line(conn)
	
        if data == '1':
            login(conn)
            break

        elif data == '2':
            print("register")
            break

        else:
            errmsg = ERRMSG_OPTION

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
            get_main_menu(connection)
        finally:
            # Close the connection
            connection.send(COR_DEFAULT) # colored white(normal)
            connection.close()
            print("closed")

if __name__ == "__main__":
    server()
