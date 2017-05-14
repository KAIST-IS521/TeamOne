from util import *

def user_check_balance(conn, user):
    # TODO: SQL request and get balance
    balance = 0

    print_logo(conn)
    conn.sendall(" [ Check Balance ]\n" +
                 " Hello, " + user + ".\n\n" + COR_RESULT + 
                 " Balance: " + str(balance) + " won\n\n" + COR_BASE)
        
    conn.send(" Enter any key to return to the previous menu -> ")
        
    # get any input from user to return previous menu
    data = recv_line(conn)
