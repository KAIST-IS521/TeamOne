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

def recv_line(conn):
    # recv 1 byte until get '\n'
    data = []
    while True:
        byte = conn.recv(1)
        if byte == '\n':
            break
        data.append(byte)
    return ''.join(data)
