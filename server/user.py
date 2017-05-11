import re
from main import *

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

def user_check_history(conn, user):
    print("history")

def user_transfer(conn, user):
    print_logo(conn)
    conn.sendall(" [ Transfer ]\n" + 
                 " Hello, " + user + ".\n\n" +
                 " Please enter required information for transfer.\n\n")
  
    receiver = get_receiver(conn)

    #TODO: confirm valid receiver or not
    
    amount = get_amount(conn)

    #TODO: confirm balance > amount to transfer

def get_receiver(conn):
    while True:
        conn.send(" * Receiver -> ")

        # get receiver from user
        data = recv_line(conn)
        
    	#remove all space existing in receiver
        regex = re.compile(r'\s+')
        data = re.sub(regex, '', data)

        if data == '':
            conn.send(ERRMSG_RECV_NULL)
        elif len(data) > LEN_USERNAME:
            conn.send(ERRMSG_RECV_LEN)
        else:
            return data

def get_amount(conn):
    while True:
        conn.send(" * Amount to transfer -> ")

        # get amount from user
        data = recv_line(conn)
        
    	#remove all space existing in receiver
        regex = re.compile(r'\s+')
        data = re.sub(regex, '', data)

        if data == '':
            conn.send(ERRMSG_WON_NULL)
        else:
            return data

def user_mypage(conn, user):
    print("edit")

