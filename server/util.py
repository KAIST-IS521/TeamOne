from const import *

def print_logo(conn):
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

def recv_line(conn):
    # recv 1 byte until get '\n'
    data = []
    while True:
        byte = conn.recv(1)
        if byte == b'\n':
            break
        data.append(byte)
    return b''.join(data).decode('utf-8')

# Get encrypted random
def recv_encrypted(conn):
    data = []
    end_string = b'-----END PGP MESSAGE-----\n'
    while True:
        byte_data = conn.recv(1024)
        data.append(byte_data)
        if(byte_data == end_string):
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
