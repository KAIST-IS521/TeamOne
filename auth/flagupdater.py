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
        return False

    # JSON
    jd = json.loads(plain)
    data = jd['signer']+":"+jd['newflag']

    # Is signer TA
    if not isTA(jd['signer']):
        print("Not TA. " + jd['signer'] + " kicked!")
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
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connetions
    sock.listen(1)
    
    while True:
        connection, client_address = sock.accept()
        print('accepting up on %s port %s' % client_address)

        try:
            data = []
            while True:
                byte = connection.recv(1)
                if byte == b'' :
                    break
                data.append(byte)
            if not saveflag(b''.join(data)) :
                print ("invalid update message")
        finally:
            # Close the connection
            connection.close()
            print("closed")

if __name__ == "__main__":
    initialize_gpg()
    try:
        server()

        # test for verification of newflag, 
        # signature has sign only.
#        saveflag("{\n\"signer\" : \"james010kim\", \"newflag\" : \"thisisnewflag\", \"signature\" : \"iQEcBAEBAgAGBQJZGtwdAAoJEPCPYHY8FuWzfgoIAJ1/inUc4DqyY/20NmRW8UuQfOo/4Hv3a9gx4M8kYIrpEZJVowxvoVmuV8bEIlROHZZAlos2KniLk9yMunDSSoK+SpKg6fVET3l3q6O16kqQ6CIqFUch9B5bYxCNWPj9E65Cq8Spq7mhUmTbmeVvjNCXU/LZ7y4pzh8RX5oWSL3mkeiZTh+vB3h6AzdBcEdQHuSZDvctmsjAnLM1Xj2itoV3ZIebenFH3RXOew4CpmqiI8FP3rfuWG4x9XjXh9oxgG6ojImsJSxsMjT8efhpqYuvOF5YsxG5EsQK8nnkt2Lfs6Bxf01klwDfRpJENFF3R32C4fSUmsVKeARzgtFf1+U==rqA8\" }")	
        # signature has data and sign.
#        saveflag("{\n\"signer\" : \"james010kim\", \"newflag\" : \"thisisnewflag\", \"signature\" : \"owEBVgGp/pANAwACAfCPYHY8FuWzAawmYgdtc2cudHh0WR0C4GphbWVzMDEwa2ltOnRoaXNpc25ld2ZsYWeJARwEAAECAAYFAlkdAuAACgkQ8I9gdjwW5bPBEAgAsSGaZtJ03XxVcTgKlLBu+LRymtMRApc6I0I5e0H/9/5WDkLrPsUJ8G72fFu2oQ97sl/V9hUeT90xgqSHFgfZuxRanybTGbSNiJ1g56RY1B7Yszf+1kutgOZnab4xNAeadadzNOD2KYlrwfQFNVT2cVl4679oG17XRiQLJOIR+gAKIvjE0O/U+P8tQ6Yhe5mzhx9dbwawV7nUW9fvfQNQhPMR7F8Ek0wHkBwVfG2qbRjLuuAULA21BHHxQijyjpOdaTX9bhPURBQ20hHPfy1oWxwGHNbW17QoNV53tWHeL3UZ33g3/5iFOB1uuXGGTmpkOGd5wMC8b6RMR9qdC3lKjw==\" }")	
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
