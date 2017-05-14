from util import *
from datetime import datetime
import re

def print_transfer(conn, user, receiver, amount, date, balance):
    conn.sendall(COR_RESULT +
                 " # Sender: " + user + "\n" +
                 " # Receiver: " + receiver + "\n" +
                 " # Transfer Amount: " + amount + " Won\n" +
                 " # Transfer Date: " + date + "\n")
    if balance:
        conn.sendall(" # Balance after transfer: " + str(balance) + "\n\n" + 
                COR_BASE)
    else:
        conn.sendall("\n" + COR_BASE)

def user_transfer(conn, user):
    receiver = get_receiver(conn, user)
    amount = get_amount(conn, user, receiver)

    # get current transfer time
    date = datetime.now().strftime('%Y-%m-%d')
    
    # get confrim about transfer
    errmsg = ""
    while True:
        print_logo(conn)

        # print history & confirm message
        conn.sendall(" [ Transfer ]\n" + 
                     " Hello, " + user + ".\n\n" +
                     " Please enter required information for transfer.\n\n" +
                     " * Receiver -> " + receiver + "\n" +
                     " * Amount to transfer -> " + amount + "\n" +
                     "\n Please confirm the following transfer details.\n\n")
        
        print_transfer(conn, user, receiver, amount, date, None)

        if errmsg:
            conn.send(errmsg)
            
        conn.send(" Would you like to transfer? (Y/N) -> ")

        # get input from usr
        data = recv_line(conn)
        data = data.upper()

        # Y -> do transfer
        if data == 'Y':
            transfer_success(conn, user, receiver, amount)
            return
        
        # N -> cancel the transfer
        elif data == 'N':
            transfer_cancel(conn, user)
            return

        else:
            errmsg = ERRMSG_OPTION

def transfer_success(conn, user, receiver, amount):
    # TODO: confirm valid receiver
    # TODO: confirm  amount < balance
    # TODO: if valid, do transfer 
    # TODO: add UI for fail to transfer

    balance = 0 # TODO: get balance from DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print_logo(conn)
    conn.sendall(" [ Transfer ] \n" +
                 " Hello, " + user + ".\n\n")

    # print transfer details
    print_transfer(conn, user, receiver, amount, date, balance)
    conn.sendall(COR_SUCCESS + 
                 "\n ** Transfer complete successfully! **\n\n" + COR_BASE)
        
    conn.send(" Enter any key to return to the previous menu -> ")
    
    # get input from user to return to previous menu
    data = recv_line(conn)

def transfer_cancel(conn, user):
    balance = 0 # TODO: get balance from DB

    print_logo(conn)
    conn.sendall(" [ Transfer ] \n" + 
                 " Hello, " + user + ".\n\n" + COR_ERRMSG + 
                 " ** Transfer Canceled ** \n\n" + COR_RESULT +
                 " Balance: " + str(balance) + " won\n\n" + COR_BASE)

    conn.send(" Enter any key to return to the previous menu -> ")

    # get input from user to return to previous menu
    data = recv_line(conn)
        
def get_receiver(conn, user):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(" [ Transfer ]\n" + 
                     " Hello, " + user + ".\n\n" +
                     " Please enter required information for transfer.\n\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(" * Receiver -> ")

        # get receiver from user
        data = recv_line(conn)
        
        regex = re.compile(REGEX_USERNAME)

        if data == '':
            errmsg = ERRMSG_RECV_NULL
        elif regex.match(data) is None:
            errmsg = ERRMSG_RECV_INVAL
        else:
            return data

def get_amount(conn, user, target):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(" [ Transfer ]\n" + 
                     " Hello, " + user + ".\n\n" +
                     " Please enter required information for transfer.\n\n" +
                     " * Receiver -> " + target + "\n")
        
        if errmsg:
            conn.send(errmsg)

        conn.send(" * Amount to transfer -> ")

        # get amount from user
        data = recv_line(conn)
        
        # check amount is valid or not
        regex = re.compile(REGEX_AMOUNT)

        if data == '':
            errmsg = ERRMSG_WON_NULL
        elif regex.match(data) is None:
            errmsg = ERRMSG_WON_INVAL
        else:
            return data
