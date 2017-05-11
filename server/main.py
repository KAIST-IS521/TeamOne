import socket, sys, re
from const import *
from user import *

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

def get_username(conn):
    while True:
        conn.send(" * Username -> ")

        # get username from user
        data = recv_line(conn)
       
        # remove all space existing in username
        regex = re.compile(r'\s+')
        data = re.sub(regex, '', data)

        if data == '':
            conn.send(ERRMSG_USER_NULL)
        elif len(data) > LEN_USERNAME:
            conn.send(ERRMSG_USER_LEN)
        else:
            return data

def get_password(conn):
    while True:
        conn.send(" * Password -> ")

        # get password from user
        data = recv_line(conn)
        
        if data == '':
            conn.send(ERRMSG_PW_NULL)
        elif len(data) > LEN_PASSWORD:
            conn.send(ERRMSG_PW_LEN)
        else:
            return data

def login(conn):
    print_logo(conn)
    conn.sendall(" [ Login ]\n" +
                 " Please input username and password. \n\n")

    # get & store username and password
    name = get_username(conn)
    pw = get_password(conn)

    # TODO SQL request and confirm

    login_success(conn, name)

def login_success(conn, user):
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

def get_option(conn):
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

def recv_line(conn):
    # recv 1 byte until get '\n'
    data = []
    while True:
        byte = conn.recv(1)
        if byte == '\n':
            break
        data.append(byte)
    return ''.join(data)

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
