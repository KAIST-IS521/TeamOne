from main import *

def user_check_balance(conn, user):
    # TODO: SQL request and get balance
    balance = 0

    print_logo(conn)
    conn.sendall(" Hello, " + user + ".\n\n" +
                 COR_RESULT + " Balance: " + str(balance) + " won\n\n" +
                 COR_BASE)

    while True:
        conn.send(" Enter 'Y' to return to the previous menu -> ")
        
        # get input from user
        data = recv_line(conn)
        data = data.upper()

        if data == 'Y':
            break

def user_check_history(conn, user):
    print("history")

def user_transfer(conn, user):
    print("transfer")

def user_mypage(conn, user):
    print("edit")

