import re
from util import *

def user_mypage(conn, user, obj):
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
        
        # check password ivalid or not
        if data == '':
            errmsg = ERRMSG_PW_NULL
        elif obj.match_id_pw(user, data) == False:
            errmsg = ERRMSG_PW_WRONG
        else:
            break

    errmsg = ""
    while True:
        print_logo(conn)
        conn.sendall(b" [ My Account ]\n" +
                     b" Hello, " + user.encode() + b".\n\n" +
                     b" 1. Edit user info \n" +
                     b" 2. Remove account \n" +
                     b" 3. Previous menu \n\n")
        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.send(b" What would you like to do? -> ")

        # get an option from user
        data = recv_line(conn)

        if data == '1':
            return user_edit_info(conn, user, obj)
            
        elif data == '2':
            return user_remove_account(conn, user, obj)

        elif data == '3':
            return 0
        else:
            errmsg = ERRMSG_OPTION

def user_edit_info(conn, user, obj):
    # get every user info from DB
    info = obj.get_every_user_info(user)

    init_msg = (b" [ Edit User Info ]\n" + 
                b" Hello, " + user.encode() + b".\n\n" +
                b" 1. Password \n" +
                b" 2. Email : " + info['email'].encode() + b"\n" +
                b" 3. Phone number : " + info['mobile'].encode() + b"\n" +
                b" 4. Previous menu\n\n")
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(init_msg)
        
        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.sendall(b" What information would you like to edit? -> ")
        
        # get an option from user
        data = recv_line(conn)

        # if edit password -> login again
        if data == '1': # password edit
            init_msg += (b" What information would you like to edit? -> " +
                    data.encode() + b"\n\n")
            return edit_info(conn, user, 1, init_msg, info, obj)

        elif data == '2': # email edit
            init_msg += (b" What information would you like to edit? -> " +
                    data.encode() + b"\n\n")
            edit_info(conn, user, 2, init_msg, info, obj)
            return 0

        elif data == '3': # phone number edit
            init_msg += (b" What information would you like to edit? -> " +
                    data.encode() + b"\n\n")
            edit_info(conn, user, 3, init_msg, info, obj)
            return 0

        elif data == '4': # go to previous menu
            return 0

        else:
            errmsg = ERRMSG_OPTION

def edit_info(conn, user, option, msg, info, obj):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(msg)
        
        if errmsg:
            conn.send(errmsg)

        if option == 1: # password edit
            new_pw = get_password(conn, msg, 1)
            msg += (b" * New Password -> " + new_pw.encode() + b"\n\n")
            info['user_pw'] = new_pw
            break

        elif option == 2: # email edit
            conn.sendall(b" * New Email -> ")

            # get email from user
            data = recv_line(conn)

            regex = re.compile(REGEX_EMAIL)
            
            if data == '':
                errmsg = ERRMSG_EMAIL_NULL
            elif len(data) > 45:
                errmsg = ERRMSG_EMAIL_LEN
            elif regex.match(data) == None:
                errmsg = ERRMSG_EMAIL_INVAL
            else:
                new_mail = data
                msg += (b" * New Email -> " + new_mail.encode() + b"\n\n")
                info['email'] = new_mail
                break

        elif option == 3: # phone number edit
            conn.sendall(b" * New Phone Number (digit only) -> ")

            # get phone number from user
            data = recv_line(conn)
            
            regex = re.compile(REGEX_PHONE)
	    
            if data == '':
                errmsg = ERRMSG_PHONE_NULL
            elif regex.match(data) == None:
                errmsg = ERRMSG_PHONE_INVAL
            else:
                new_phone = data
                msg += (b" * New Phone Number (digit only) -> " +
                        new_phone.encode() + b"\n\n")
                info['mobile'] = new_phone
                break

    errmsg = ""
    while True:
        print_logo(conn)
        conn.sendall(msg)
        
        if errmsg:
            conn.send(errmsg)
        errmsg = ""
        
        conn.send(b" Would you like to save your modification? (Y/N) -> ")
        
        # get input from user
        data = recv_line(conn)
        data = data.upper()

        # Y -> do modify
        if data == 'Y':
            # store entered information in DB 
            ret = obj.store_user_info_modification(user, info)

            if ret == True:
                conn.sendall(COR_SUCCESS +
                        b"\n ** Modification successfully completed! **\n\n" 
                        + COR_BASE)
            
                conn.send(b" Enter any key to return to the previous menu -> ")
                data = recv_line(conn)
                return 1
            else:
                # DB error : cancel modification
                conn.sendall(COR_ERRMSG +
                        b"\n ** Modification Canceled **\n\n" + COR_BASE)
                conn.send(b" Enter any key to return to the previous menu -> ")
                data = recv_line(conn)
                return 0

        # N -> calcel the modification
        elif data == 'N':
            conn.sendall(COR_ERRMSG +
                    b"\n ** Modification Canceled **\n\n" + COR_BASE)
            
            conn.send(b" Enter any key to return to the previous menu -> ")
            data = recv_line(conn)
            return 0
        else:
            errmsg = ERRMSG_OPTION

def user_remove_account(conn, user, obj):
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
            remove_success(conn, user, obj)
            return 1
        
        # N -> cancel deletion
        elif data == 'N':
            conn.send(b"\n ** Removing Account Canceled ** \n" +
                      b"\n Enter any key to return to the previous menu -> ")
            data = recv_line(conn)
            return 0

        else:
            errmsg = ERRMSG_OPTION

def remove_success(conn, user, obj):
    # remove correspoding account from DB
    ret = obj.remove_user_account(user)
    
    if ret == True:
        conn.sendall(b"\n Your account is removed successfully.\n" +
                     b" Thank you for using our bank so far.\n\n" +
                     b" Enter any key to return to the main menu -> ")
    else:
        conn.send(b"\n ** Removing Account Canceled ** \n" +
                  b"\n Enter any key to return to the previous menu -> ")
    
    data = recv_line(conn)
