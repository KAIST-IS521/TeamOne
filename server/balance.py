from util import *

def user_check_balance(conn, user):
    # TODO: SQL request and get balance
    balance = 0

    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(" [ Check Balance ]\n" +
                     " Hello, " + user + ".\n\n" + COR_RESULT + 
                     " Balance: " + str(balance) + " won\n\n" + COR_BASE)
        
        if errmsg:
            conn.send(errmsg)

        conn.send(" Enter 'Y' to return to the previous menu -> ")
        
        # get input from user
        data = recv_line(conn)
        data = data.upper()

        if data == 'Y':
            return
        else:
            errmsg = ERRMSG_OPTION
