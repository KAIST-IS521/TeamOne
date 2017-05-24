import socket, sys, re, base64, os, inspect
from threading import Thread
from .const import *
from .util import *
from .balance import *
from .history import *
from .transfer import *
from .mypage import *

# get current & parent execution path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from db import utils
from auth import auth

# global variable
input_passphrase = ""

# PGP-authentication for registration
def pgp_auth(conn, obj):
    init_msg = (b" [ PGP Authentication ]\n" +
                b" Please input the following information.\n\n")
    errmsg = ""

    # Get github_id
    while True:
        print_logo(conn)
        conn.sendall(init_msg)

        if errmsg:
           conn.send(errmsg)
        errmg = ""

        # get github id from user
        github_id = get_github_id(conn, init_msg, 1)
        init_msg += (b" * GitHub ID -> " + github_id.encode() + b"\n")

        # Initialize GPG
        initialize_gpg()

        # Check if the inputted github ID is valid
        if(check_registered(github_id)):
            # Generate random
            rand = generate_random(github_id)

            # Generate challenge for the given github_id
            challenge = generate_challenge(github_id, rand, input_passphrase)
            
            # Send challenge and receive the response from the user
            response = get_response(conn, challenge, 1)

            # Decrypt the encrypted random
            decrypted_rand = verify_response(github_id, response, 
                    input_passphrase)

            # Check if the sent and received random is identical
            if(hex(rand) == decrypted_rand.rstrip()):
                register(conn, github_id, obj)
                break
            else:
                init_msg += (b"PGP authentication failed!\n\n")
                continue

        else:
            init_msg += (b"GitHub ID is NOT registered!\n\n")
            continue

def register(conn, github_id, obj):
    init_msg = (b" [ Register ]\n" +
                b" Please input the following information.\n\n")
    errmsg = ""
    cnt = 0 # count for register process

    while True:
        print_logo(conn)
        conn.sendall(init_msg)

        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        if cnt == 0:
            # get user name
            name = get_username(conn, init_msg, obj, 1)
            init_msg += (b" * Username -> " + name.encode() + b"\n")
            cnt += 1 # username OK
            continue

        if cnt == 1:
            # get password
            pw = get_password(conn, init_msg, 0)
            init_msg += (b" * Password -> " + pw.encode() + b"\n")
            cnt += 1 # password OK
            continue

        if cnt == 2:
            # get email
            conn.sendall(b" * Email -> ")
            data = recv_line(conn)

            regex = re.compile(REGEX_EMAIL)

            if data == '':
                errmsg = ERRMSG_EMAIL_NULL
            elif len(data) > 45:
                errmsg = ERRMSG_EMAIL_LEN
            elif regex.match(data) == None: 
                errmsg = ERRMSG_EMAIL_INVAL
            else:
                email = data
                init_msg += (b" * Email -> " + email.encode() + b"\n")
                cnt += 1 # email OK
            continue

        if cnt == 3:
            # get phone number
            conn.sendall(b" * Phone number (digit only) -> ")
            data = recv_line(conn)

            regex = re.compile(REGEX_PHONE)

            if data == '':
                errmsg = ERRMSG_PHONE_NULL
            elif regex.match(data) == None:
                errmsg = ERRMSG_PHONE_INVAL
            else:
                phone = data
                init_msg += (b" * Phone number (digit only) -> " +
                        phone.encode() + b"\n")
                break # all processes are done

    errmsg = ""
    while True:
        # provide 1000 won if new customer
        if obj.get_reg_flag(github_id) == 0:
            balance = 1000
        else:
            balance = 0

        # show entered user information & welcome
        print_logo(conn)
        conn.sendall(b" [ Register ] \n" +
                     b" Your entered information are as follows.\n\n" +
                     COR_RESULT +
                     b" # Username: " + name.encode() + b"\n" +
                     b" # Password: " + pw.encode() + b"\n" +
                     b" # Github ID: " + github_id.encode() + b"\n" +
                     b" # Email: " + email.encode() + b"\n" +
                     b" # Phone number: " + phone.encode() + b"\n" +
                     b" # Balance: " + str(balance).encode() + b" Won\n\n" +
                     COR_BASE)
        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.send(b" Would you like to register? (Y/N) -> ")

        # get input from user
        data = recv_line(conn)
        data = data.upper()

        # Y -> do register
        if data == 'Y':
            # store entered information in DB
            ret = obj.store_user(name, pw, github_id, email, phone, balance)

            # if fail to store in DB
            if ret == False:
                conn.sendall(COR_ERRMSG +
                        b"\n ** Register Canceled **\n\n" + COR_BASE)
                conn.send(b" Enter any key to return to the previous menu -> ")
                data = recv_line(conn)
                return
            # if succeed to store in DB
            else:
                conn.sendall(COR_SUCCESS +
                        b"\n ** Register complete successfully! **\n\n" + 
                        COR_BASE)
                conn.send(b" Enter any key to return to the previous menu -> ")
                data = recv_line(conn)
                return

        # N -> calcel the register
        elif data == 'N':
            conn.sendall(COR_ERRMSG +
                    b"\n ** Register Canceled **\n\n" + COR_BASE)

            conn.send(b" Enter any key to return to the previous menu -> ")
            data = recv_line(conn)
            return
        else:
            errmsg = ERRMSG_OPTION

# Get response from user for PGP authentication
def get_response(conn, msg, flag):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(msg)

        if errmsg:
            conn.send(errmsg)

        conn.send(b"\n * Encrypted response ->\n")

        # Get encrypted random number
        data = recv_encrypted(conn)

        return data

# get github ID from user for PGP authentication
def get_github_id(conn, msg, flag):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(msg)

        if errmsg:
            conn.send(errmsg)

        conn.send(b" * GitHub ID -> ")

        # get github id from user
        data = recv_line(conn)

        # ID : lowerletter, upperletter, number
        regex = re.compile(REGEX_USERNAME)

        if data == '':
            errmsg = ERRMSG_USER_NULL
        elif regex.match(data) == None:
            errmsg = ERRMSG_USER_INVAL
        else:
            return data

def get_username(conn, msg, obj, flag):
    errmsg = ""

    while True:
        print_logo(conn)
        conn.sendall(msg)

        if errmsg:
            conn.send(errmsg)

        conn.send(b" * Username -> ")

        # get username from user
        data = recv_line(conn)

        # ID : lowerletter, upperletter, number
        regex = re.compile(REGEX_USERNAME)

        if data == '':
            errmsg = ERRMSG_USER_NULL
        elif regex.match(data) == None:
            errmsg = ERRMSG_USER_INVAL
        # if user entered already used ID in register
        elif flag == 1 and obj.is_existing_id(data) == True:
            errmsg = ERRMSG_USER_USED
        else:
            return data

def login(conn, obj):
    errmsg = ""

    while True:
        # get & store username and password
        msg = (b" [ Login ]\n" +
               b" Please input username and password. \n\n")

        if errmsg:
            msg += (errmsg + b"\n")

        # get user ID
        name = get_username(conn, msg, obj, 0)

        msg += (b" * Username -> " + bytes(name.encode()) + b"\n")
        pw = get_password(conn, msg, 0)

        # SQL request and confirm
        ret = obj.match_id_pw(name, pw)

        # if ID and pw are matched -> go to usermenu
        if ret == True:
            account_num = obj.get_account_num(name)
            get_user_menu(conn, name, str(account_num), obj)
            return
       # if id or pw is not correct
        else:
            errmsg = ERRMSG_LOGIN

def get_user_menu(conn, user, account_num, obj):
    errmsg = ""

    while True:
        # print user menu
        print_logo(conn)
        conn.sendall(b" [ User Menu ]\n" +
                     b" Hello, " + bytes(user.encode()) + b" (" +
                     account_num.encode() + b").\n\n" +
                     b" 1. Check balance \n" +
                     b" 2. Check transaction history \n" +
                     b" 3. Transfer \n" +
                     b" 4. Edit user info & Remove account \n" +
                     b" 5. Logout \n\n")

        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.send(b" What would you like to do? -> ")

        # get an option from user
        data = recv_line(conn)

        if data == '1':
            user_check_balance(conn, user, account_num, obj)

        elif data == '2':
            user_check_history(conn, user, account_num, obj)

        elif data == '3':
            user_transfer(conn, user, account_num, obj)

        elif data == '4':
            ret = user_mypage(conn, user, account_num, obj)
            # if user remove account or change password -> go to main
            if ret == 1: return

        elif data == '5': # logout -> go to main
            return

        else:
            errmsg = ERRMSG_OPTION

def get_main_menu(conn, addr, obj):
    errmsg = ""

    while True:
        # print main screen
        print_logo(conn)
        conn.sendall(b" Hello, customer.\n" +
                     b" 1. Login\n" +
                     b" 2. Register\n" +
                     b" 3. Terminate\n\n")

        if errmsg:
            conn.send(errmsg)
        errmsg = ""

        conn.sendall(b" What would you like to do? -> ")

        # get an option from user
        data = recv_line(conn)

        if data == '1':
            login(conn, obj)

        elif data == '2':
            pgp_auth(conn, obj)

        elif data == '3': # terminate program
            # close the connection
            conn.send(COR_DEFAULT) # colored white(normal)
            conn.close()
            print("[Terminated] "+ addr[0] + " closed.")
            return

        else:
            errmsg = ERRMSG_OPTION

def handler(conn, addr):
    try:
        obj = utils.bankDB()
        get_main_menu(conn, addr, obj)

    except Exception as e:
        # Close the connection
        try:
            conn.send(COR_DEFAULT) # colored white(normal)
            conn.close()
            print("[Error] " + addr[0] + " closed.")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), 
                type(e), e)
        except:
            print("handler exception")

def server():
    thread_list = []

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 1588)
    print('starting up on %s port %s' %server_address)
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(5)

    while True:
        connection, client_addr = sock.accept()

        thread = Thread(target=handler, args=(connection, client_addr))
        thread_list.append(thread)
        thread.start()

        for thread in thread_list:
            if not thread.isAlive():
                thread_list.remove(thread)
                thread.join()
