from .util import *
from datetime import datetime
import re

def print_transfer(conn, user, receiver, amount, date, msg, balance):
    # print transfer details
    conn.sendall(COR_RESULT +
                 b" # Sender: " + user.encode() + b"\n" +
                 b" # Receiver: " + receiver.encode() + b"\n" +
                 b" # Transfer Amount: " + amount.encode() + b" Won\n" +
                 b" # Transfer Date: " + date.encode() + b"\n" +
                 b" # Transfer message: " + msg.encode() + b"\n")
    if balance:
        conn.sendall(b" # Balance after transfer: " + str(balance).encode() + 
                b"\n\n" + COR_BASE)
    else:
        conn.sendall(b"\n" + COR_BASE)

def user_transfer(conn, user, account_num, obj):
    # get receiver from user
    receiver = get_receiver(conn, user, account_num, obj)

    # get amount to transfer
    amount = get_amount(conn, user, account_num, receiver, obj)

    # get transfer message
    message = get_message(conn, user, account_num, receiver, amount)

    # get current transfer time
    date = datetime.now().strftime('%Y-%m-%d')
    
    # get confrim about transfer
    errmsg = ""
    while True:
        print_logo(conn)

        # print entered transfer details & confirm message
        conn.sendall(b" [ Transfer ]\n" + 
                     b" Hello, " + user.encode() + b" (" +
                     account_num.encode() + b").\n\n" +
                     b" Please enter required information for transfer.\n\n" +
                     b" * Receiver (user ID) -> " + receiver.encode() + b"\n" +
                     b" * Amount to transfer -> " + amount.encode() + b"\n" +
                     b" * Transfer message -> " + message.encode() + b"\n" +
                     b"\n Please confirm the following transfer details.\n\n")
        
        balance = obj.get_balance(user)
        print_transfer(conn, user, receiver, amount, date, message, None)

        if errmsg:
            conn.send(errmsg)
            
        conn.send(b" Would you like to transfer? (Y/N) -> ")

        # get input from usr
        data = recv_line(conn)
        data = data.upper()

        # Y -> do transfer
        if data == 'Y':
            ret = obj.store_transaction(user, receiver, int(amount), message)
            
            # if succeed to transfer
            if ret == True:
                transfer_success(conn, user, account_num, receiver, amount, 
                        message, obj)
            # if fail to transfer
            else:
                transfer_cancel(conn, user, account_num, obj)
            return
        
        # N -> cancel the transfer
        elif data == 'N':
            transfer_cancel(conn, user, account_num, obj)
            return

        else:
            errmsg = ERRMSG_OPTION

def transfer_success(conn, user, account_num, receiver, amount, msg, obj):
    balance = obj.get_balance(user) # get balance from DB

    # get real transfer time after getting user reconfimation
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print_logo(conn)
    conn.sendall(b" [ Transfer ] \n" +
                 b" Hello, " + user.encode() + b" (" +
                 account_num.encode() + b").\n\n")

    # print transfer details
    print_transfer(conn, user, receiver, amount, date, msg, balance)
    conn.sendall(COR_SUCCESS + 
                 b"\n ** Transfer complete successfully! **\n\n" + COR_BASE)
        
    conn.send(b" Enter any key to return to the previous menu -> ")
    
    # get input from user to return to previous menu
    data = recv_line(conn)

def transfer_cancel(conn, user, account_num, obj):
    balance = obj.get_balance(user) # get balance from DB

    # print transfer cancel message
    print_logo(conn)
    conn.sendall(b" [ Transfer ] \n" + 
                 b" Hello, " + user.encode() + b" (" +
                 account_num.encode() + b").\n\n" + COR_ERRMSG + 
                 b" ** Transfer Canceled ** \n\n" + COR_RESULT +
                 b" Balance: " + str(balance).encode() + b" won\n\n" + COR_BASE)

    conn.send(b" Enter any key to return to the previous menu -> ")

    # get input from user to return to previous menu
    data = recv_line(conn)
        
def get_receiver(conn, user, account_num, obj):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(b" [ Transfer ]\n" + 
                     b" Hello, " + user.encode() + b" (" +
                     account_num.encode() + b").\n\n" +
                     b" Please enter required information for transfer.\n\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(b" * Receiver (user ID) -> ")

        # get receiver from user
        data = recv_line(conn)
        
        regex = re.compile(REGEX_USERNAME)

        if data == '':
            errmsg = ERRMSG_RECV_NULL
        elif (regex.match(data) == None or
                obj.is_existing_id(data) == False or
                user == data): # if sender == receiver
            errmsg = ERRMSG_RECV_INVAL
        else:
            return data

def get_amount(conn, user, account_num, target, obj):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(b" [ Transfer ]\n" + 
                     b" Hello, " + user.encode() + b" (" +
                     account_num.encode() + b").\n\n" +
                     b" Please enter required information for transfer.\n\n" +
                     b" * Receiver (user ID) -> " + target.encode() + b"\n")
        
        if errmsg:
            conn.send(errmsg)

        conn.send(b" * Amount to transfer -> ")

        # get amount from user
        data = recv_line(conn)
        
        # check amount is valid or not
        regex = re.compile(REGEX_AMOUNT)

        # amount should be not zero and lower than balance
        if data == '':
            errmsg = ERRMSG_WON_NULL
        elif regex.match(data) == None:
            errmsg = ERRMSG_WON_INVAL
        elif int(data) == 0:
            errmsg = ERRMSG_WON_INVAL
        elif int(data) > obj.get_balance(user):
            errmsg = ERRMSG_WON_LIMIT
        else:
            return data

def get_message(conn, user, account_num, target, amount):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(b" [ Transfer ]\n" + 
                     b" Hello, " + user.encode() + b" (" +
                     account_num.encode() + b").\n\n" +
                     b" Please enter required information for transfer.\n\n" +
                     b" * Receiver (user ID) -> " + target.encode() + b"\n"
                     b" * Amount to transfer -> " + amount.encode() + b"\n")
        
        if errmsg:
            conn.send(errmsg)

        conn.sendall(b" * Transfer message -> ")

        # get amount from user
        data = recv_line(conn)
        
        if data == '':
            errmsg = ERRMSG_MSG_NULL
        elif len(data) > LEN_MSG:
            errmsg = ERRMSG_MSG_LEN
        else:
            return data
