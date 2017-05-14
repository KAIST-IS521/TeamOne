import socket, sys, re
from threading import Thread
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
        conn.sendall(b" [ Login ]\n" +
                     b" Please input username and password. \n\n")

        if errmsg:
            conn.send(errmsg)

        conn.send(b" * Username -> ")

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
        conn.sendall(b" [ Login ]\n" +
                     b" Please input username and password. \n\n" +
                     b" * Username -> " + bytes(name.encode()) + b"\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(b" * Password -> ")

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
        conn.sendall(b" [ User Menu ]\n" +
                     b" Hello, " + bytes(user.encode()) + b".\n\n" +
                     b" 1. Check balance \n" + 
                     b" 2. Check transaction history \n" +
                     b" 3. Transfer \n" +
                     b" 4. Edit user info & Remove account \n" +
                     b" 5. Logout \n\n")

        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.send(b" What would you like to do? -> ")
        
        # get an option from user
        data = recv_line(conn)

        if data == '1':
            user_check_balance(conn, user)
        elif data == '2':
            user_check_history(conn, user)
        elif data == '3':
            user_transfer(conn, user)
        elif data == '4':
            ret = user_mypage(conn, user)
            if ret == 1: return # if user remove account -> go to main
        elif data == '5': # logout -> go to main
            return
        else:
            errmsg = ERRMSG_OPTION

def get_main_menu(conn, addr):
    errmsg = ""

    while True:
        # print main screen
        print_logo(conn)
        conn.sendall(b" Hello, customer.\n" +
                     b" 1. Login\n" +
                     b" 2. Register\n" +
                     b" 3. Terminate\n\n")

        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.sendall(b" What would you like to do? -> ")
    
        # get an option from user
        data = recv_line(conn)
        
        if data == '1':
            login(conn)

        elif data == '2':
            print("register")

        elif data == '3': # terminate program
            # close the connection
            conn.send(COR_DEFAULT) # colored white(normal)
            conn.close()
            print("[Terminated] "+ addr[0] + " closed.")
            return

        else:
            errmsg = ERRMSG_OPTION

def handler(conn, addr):
    try:
        get_main_menu(conn, addr)

    except:
        # Close the connection
        conn.send(COR_DEFAULT) # colored white(normal)
        conn.close()
        print("[Error] " + addr[0] + " closed.")

def server():
    thread_list = []

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 1588)
    print('starting up on %s port %s' %server_address)
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(5)
    
    while True:
        connection, client_addr = sock.accept()

        thread = Thread(target=handler, args=(connection, client_addr))
        thread_list.append(thread)
        thread.start()

        for thread in thread_list:
            if not thread.isAlive():
                thread_list.remove(thread)
                thread.join()

if __name__ == "__main__":
    try:
        server()
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
