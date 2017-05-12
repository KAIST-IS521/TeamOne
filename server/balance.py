from func import *

def user_check_balance(conn, user):
    # TODO: SQL request and get balance
    balance = 0

    print_logo(conn)
    conn.sendall(" [ Check Balance ]\n" +
                 " Hello, " + user + ".\n\n" +
                 COR_RESULT + " Balance: " + str(balance) + " won\n\n" +
                 COR_BASE)

    while True:
        conn.send(" Enter 'Y' to return to the previous menu -> ")
        
        # get input from user
        data = recv_line(conn)
        data = data.upper()

        if data == 'Y':
            break
