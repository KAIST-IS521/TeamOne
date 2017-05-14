from util import *

def user_mypage(conn, user):
    
    # get password for confirmation
    errmsg = ""
    while True:
        print_logo(conn)
        
        conn.sendall(b" [ Identity Verification ]\n" +
                     b" Please enter password for confirmation.\n\n")
        
        if errmsg:
            conn.send(errmsg)
                     
        conn.sendall(b" * Password -> ")
        data = recv_line(conn)
        
        # TODO: check password valid or not
        if data == '':
            errmsg = ERRMSG_PW_NULL
        else:
            break

    errmsg = ""
    while True:
        print_logo(conn)
        conn.sendall(b" [ My Account ]\n" +
                     b" Hello, " + user.encode() + b".\n\n" +
                     b" 1. Edit user info \n" +
                     b" 2. Remove account \n\n")
        if errmsg:
            conn.send(errmsg)

        conn.send(b" What would you like to do? -> ")

        # get an option from user
        data = recv_line(conn)

        if data == '1':
            user_edit_info(conn, user)
            errmsg = ""
            return 0
        elif data == '2':
            errmsg = ""
            return user_remove_account(conn, user)
        else:
            errmsg = ERRMSG_OPTION

def user_edit_info(conn, user):
    # TODO: make UI after DB construction
    print("edit_info")
    
def user_remove_account(conn, user):
    errmsg = ""

    while True:
        print_logo(conn)

        # print history & confirm message
        conn.sendall(b" [ Remove Account ]\n" + 
                     b" Hello, " + user.encode() + b".\n\n")
        if errmsg:
            conn.send(errmsg)
            
        conn.sendall(COR_ERRMSG +
                b" Are you ABSOLUTELY sure to remove the account? (Y/N) -> ")

        # get input from usr
        data = recv_line(conn)
        data = data.upper()

        conn.send(COR_BASE)
        # Y -> remove account
        if data == 'Y':
            remove_success(conn, user)
            return 1
        
        # N -> cancel deletion
        elif data == 'N':
            conn.send(b"\n ** Removing Account Canceled ** \n" +
                      b"\n Enter any key to return to the previous menu -> ")
            data = recv_line(conn)
            return 0

        else:
            errmsg = ERRMSG_OPTION

def remove_success(conn, user):
    # TODO: remove correspoding account from DB
    
    conn.sendall(b"\n Your account is removed successfully.\n" +
                 b" Thank you for using our bank so far.\n\n" +
                 b" Enter any key to return to the main menu -> ")
    
    data = recv_line(conn)
