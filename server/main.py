import socket, sys, re, base64
sys.path.append('/home/vagrant/TeamOne/auth')
from threading import Thread
from const import *
from util import *
from balance import *
from history import *
from transfer import *
from mypage import *
from auth import *

# PGP-authentication for registration
def pgp_auth(conn):
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
            challenge = generate_challenge(github_id, rand)
	
	    # Send challenge and receive the response from the user
            response = get_response(conn, challenge, 1)
     
            # Decrypt the encrypted random
            decoded_response = base64.b64decode(response)
            decrypted_rand = verify_response(github_id, decoded_response)        

            # Check if the sent and received random is identical
            if(hex(rand) == decrypted_rand):
                register(conn)
                break
            else:
                init_msg += (b"PGP authentication failed!\n\n")
                continue 
          
        else:
            init_msg += (b"GitHub ID is NOT registered!\n\n")
            continue

def register(conn):
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
            name = get_username(conn, init_msg, 1)
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
            conn.sendall(b" * Phone number (ex. 01x-xxxx-xxxx) -> ")
            data = recv_line(conn)

            regex = re.compile(REGEX_PHONE)

            if data == '':
                errmsg = ERRMSG_PHONE_NULL
            elif regex.match(data) == None:
                errmsg = ERRMSG_PHONE_INVAL
            else:
                phone = data
                init_msg += (b" * Phone number (ex. 01x-xxxx-xxxx) -> " +
                        phone.encode() + b"\n")
                break # all processes are done
    
    errmsg = ""
    while True:
        # TODO: get balance
        balance = 0

        # show entered user information & welcome
        print_logo(conn)
        conn.sendall(b" [ Register ] \n" + 
                     b" Your entered information are as follows.\n\n" +
                     COR_RESULT +
                     b" # Username: " + name.encode() + b"\n" +
                     b" # Password: " + pw.encode() + b"\n" +
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
            # TODO: store entered information in DB 
            conn.sendall(COR_SUCCESS +
                    b"\n ** Register complete successfully! **\n\n" + COR_BASE)
            
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

        conn.send(b"\n * Encrypted response -> ")

        # get github id from user
        data = recv_line(conn)

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
        # TODO: if flag==1 -> is existing user(data)
        else:
            return data

def get_username(conn, msg, flag):
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
        # TODO: if flag==1 -> is existing user(data)
        else:
            return data

def login(conn):
    # get & store username and password
    msg = (b" [ Login ]\n" +
           b" Please input username and password. \n\n")
    name = get_username(conn, msg, 0)

    msg += (b" * Username -> " + bytes(name.encode()) + b"\n")
    pw = get_password(conn, msg, 0)

    # TODO SQL request and confirm

    # TODO add UI for login fail

    get_user_menu(conn, name)

def get_user_menu(conn, user):
    errmsg = ""

    while True:
        # print user menu
        print_logo(conn)
        conn.sendall(b" [ User Menu ]\n" +
                     b" Hello, " + bytes(user.encode()) + b".\n\n" +
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
            user_check_balance(conn, user)
        elif data == '2':
            user_check_history(conn, user)
        elif data == '3':
            user_transfer(conn, user)
        elif data == '4':
            ret = user_mypage(conn, user)
            if ret == 1: return # if user remove account -> go to main
        elif data == '5': # logout -> go to main
            return
        else:
            errmsg = ERRMSG_OPTION

def get_main_menu(conn, addr):
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
            login(conn)

        elif data == '2':
            pgp_auth(conn)

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
        get_main_menu(conn, addr)

    except Exception as e:
        # Close the connection
        conn.send(COR_DEFAULT) # colored white(normal)
        conn.close()
        print("[Error] " + addr[0] + " closed.")
        print(e)

def server():
    thread_list = []

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 1588)
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

if __name__ == "__main__":
    try:
        server()
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
