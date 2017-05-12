from func import *
from datetime import datetime
import re

def user_transfer(conn, user):
    print_logo(conn)
    conn.sendall(" [ Transfer ]\n" + 
                 " Hello, " + user + ".\n\n" +
                 " Please enter required information for transfer.\n\n")
  
    receiver = get_receiver(conn)

    #TODO: confirm valid receiver or not
    
    amount = get_amount(conn)

    #TODO: confirm balance > amount to transfer
    balance = 0

    # get current transfer time
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn.sendall("\n Please confirm the following transfer details.\n\n" +
                 COR_RESULT +
                 " # Sender: " + user + "\n" +
                 " # Receiver: " + receiver + "\n" +
                 " # Transfer Amount: " + amount + " won\n" +
                 " # Transfer Date: " + date + "\n\n" + COR_BASE)

    while True:
        conn.send(" Would you like to transfer? (Y/N) -> ")

        # get input from usr
        data = recv_line(conn)
        data = data.upper()

        # Y -> do transfer
        if data == 'Y':
            # TODO: transfer

            break
        
        # N -> cancel the transfer
        elif data == 'N':
            conn.send("\n ** Transfer Canceled ** \n\n")
            break

    # return to the previous menu
    while True:
        conn.send(" Enter 'Y' to return to the previous menu -> ")
         
        # get input from user
        data = recv_line(conn)
        data = data.upper()
         
        if data == 'Y':
            return

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
