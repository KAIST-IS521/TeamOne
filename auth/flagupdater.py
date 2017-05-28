#!/usr/bin/python3

import socket, sys, re, os
import json
import gnupg
import base64
import pwd, grp
from os.path import expanduser

sys.path.insert(0, '../db')
import utils

TAPUBKEY = "tapubkey/"
input_passphrase = ""

# Initialize GPG
def initialize_gpg():
    global gpg
    global flag
    global host
    homedir = expanduser("~") + "/.gnupg"
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

    # chown 'vagrant:vagrant'
    uid = pwd.getpwnam("vagrant").pw_uid
    gid = grp.getgrnam("vagrant").gr_gid
    os.chown(homedir+"/pubring.gpg", uid, gid)
    os.chown(homedir+"/pubring.gpg~", uid, gid)

def isTA(signer):
    fnames = os.listdir(TAPUBKEY)
    for name in fnames:
        if os.path.splitext(name)[0] == signer:
            return True
    return False

def decrypt(data):
    objdata = gpg.decrypt(data, passphrase=input_passphrase, always_trust=True)
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

    # Verify signature ( pgp armor is mandatory )
    ## if signature has sign only, use this armor
    pgparmor  = "-----BEGIN PGP SIGNED MESSAGE-----"+"\n"+"Hash: SHA1"+"\n\n"   
    pgparmor += data + "\n"
    pgparmor += "-----BEGIN PGP SIGNATURE-----"+"\n"+"Version: GnuPG v1"+"\n\n"
    pgparmor += jd['signature'] + "\n"
    pgparmor += "-----END PGP SIGNATURE-----"+"\n"
    ## if signature has data and sign, use following armor
    #pgparmor = "-----BEGIN PGP MESSAGE-----"+"\n"+jd['signature'])

    verified = gpg.verify(pgparmor)

    if not verified:
        print ("Error : PGP signature BAD")
        return False

    # Save flag to database
    flag = jd['newflag']
    host = jd['signer']
    print ( "NEW flag : " + flag + " from " + host )
    bank = utils.bankDB()
    try:
        bank.set_flag(flag)
    except:
        print ("Error : can't set_flag into db")

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
        if len(sys.argv) == 2:
            input_passphrase = str(sys.argv[1])
        server()
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
    except IOError as ioex:
        if ioex.errno == 13:
            print ("Error : Use 'sudo' for binding port 42")
