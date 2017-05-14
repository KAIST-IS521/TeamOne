from util import *

def user_check_balance(conn, user):
    # TODO: SQL request and get balance
    balance = 0

    print_logo(conn)
    conn.sendall(b" [ Check Balance ]\n" +
                 b" Hello, " + user.encode() + b".\n\n" + COR_RESULT + 
                 b" Balance: " + bytes(str(balance).encode()) + b" won\n\n" + COR_BASE)
        
    conn.send(b" Enter any key to return to the previous menu -> ")
        
    # get any input from user to return previous menu
    data = recv_line(conn)
