from func import *
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
