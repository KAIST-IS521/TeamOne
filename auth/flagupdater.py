#!/usr/bin/python3

import socket, sys, re, os
import json
import gnupg
import base64

sys.path.insert(0, '../db')
import utils

TAPUBKEY = "tapubkey/"
FLAGPATH = "/home/vagrant/.juicy"

# Initialize GPG
def initialize_gpg():
    global gpg
    global flag
    global host
    homedir = '/home/vagrant/.gnupg'
    try:
        gpg = gnupg.GPG(gnupghome=homedir) 
    except TypeError:
        gpg = gnupg.GPG(homedir=homedir)

    # Import TA's key
    fnames = os.listdir(TAPUBKEY)
    for name in fnames:
        with open(TAPUBKEY+name, "r") as f:
            result = gpg.import_keys(f.read())
            assert result

def isTA(signer):
    fnames = os.listdir(TAPUBKEY)
    for name in fnames:
        if os.path.splitext(name)[0] == signer:
            return True
    return False

def decrypt(data):
    objdata = gpg.decrypt(data, passphrase='', always_trust=True)		# armor is mandatory requirement
    if objdata.ok != True :
        return False
    return str(objdata)

def saveflag(recvdata):
    # Decrypt
    plain = decrypt(recvdata)
    if not plain:
        print("Error : Cannot decrypt ( Check Passphrase ! )")
        return False

    # JSON
    jd = json.loads(plain)
    data = jd['signer']+":"+jd['newflag']

    # Is signer TA
    if not isTA(jd['signer']):
        print("Error : " + jd['signer'] + " is not TA. Kicked!")
        return False

    # Verify signature, armor is mandatory.
    # signature has sign only. build an armor for gnupg
    pgparmor  = "-----BEGIN PGP SIGNED MESSAGE-----"+"\n"+"Hash: SHA1"+"\n\n"   
    pgparmor += data + "\n"
    pgparmor += "-----BEGIN PGP SIGNATURE-----"+"\n"+"Version: GnuPG v1"+"\n\n"
    pgparmor += jd['signature'] + "\n"
    pgparmor += "-----END PGP SIGNATURE-----"+"\n"
    verified = gpg.verify(pgparmor)
    # if signature has data and sign,
    #verified = gpg.verify("-----BEGIN PGP MESSAGE-----\n"+jd['signature'])		# signature has data and sign

    if not verified:
        print ("Error : PGP signature BAD")
        return False

    # Save flag to secret location)
    flag = jd['newflag']
    host = jd['signer']
    print ( "NEW flag : " + flag + " from " + host )
    with open(FLAGPATH, "w") as f:
        f.write(flag)

    return True

def server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 42)
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(1)
    
    print('Starting up on %s port %s' % server_address)

    while True:
        connection, client_address = sock.accept()
        print('Accepting up on %s port %s' % client_address)

        try:
            data = []
            while True:
                byte = connection.recv(1)
                if byte == b'' :
                    break
                data.append(byte)
            saveflag(b''.join(data))
        finally:
            # Close the connection
            connection.close()
            print("Closed")

if __name__ == "__main__":
    initialize_gpg()
    try:
        server()
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
    except IOError as ioex:
        if ioex.errno == 13:
            print ("Error : Use 'sudo' for binding port 42")
