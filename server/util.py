from .const import *

def print_logo(conn):
    try:
        conn.send(CLEAR_TERMINAL + COR_LOGO) # clear terminal & colored
        conn.sendall(b"  /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$\n" +
                     b" | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/\n" +
                     b" | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ \n" +
                     b" | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  \n" +
                     b" | $$__  $$| $$__  $$| $$  $$$$| $$  $$  \n" +
                     b" | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ \n" +
                     b" | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$\n" +
                     b" |_______/ |__/  |__/|__/  \__/|__/  \__/\n\n")

        conn.send(COR_BASE) # colored
        conn.send(b" =========================================\n")
    except:
        print("print_log exception")

def recv_line(conn):
    # recv 1 byte until get '\n'
    data = []
    while True:
        try:
            byte = conn.recv(1)
            # closed socket
            if byte == b'':
                break
        except e:
            print("socket exception")
        if byte == b'\n':
            break
        data.append(byte)
    return b''.join(data).decode('utf-8')

# Get encrypted random
def recv_encrypted(conn):
    data = []
    end_string = '-----END PGP MESSAGE-----\n'
    while True:
        try:
            byte_data = conn.recv(1024)
            if byte_data == b'':
                break
        except e:
            print("socket exception")
        data.append(byte_data)
        if(byte_data.decode().endswith(end_string)==True):
            break
    return b''.join(data).decode('utf-8')


def get_password(conn, msg, flag):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(msg)

        if errmsg:
            conn.send(errmsg)
        if flag == 0:
            conn.send(b" * Password -> ")
        elif flag == 1:
            conn.send(b" * New Password -> ")

        # get password from user
        data = recv_line(conn)
        
        if data == '':
            errmsg = ERRMSG_PW_NULL
        elif len(data) > LEN_PASSWORD:
            errmsg = ERRMSG_PW_LEN
        else:
            return data
