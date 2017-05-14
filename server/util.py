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
