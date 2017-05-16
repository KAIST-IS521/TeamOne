#!/usr/bin/python3

import socket, sys, re, json
import gnupg
import base64

# Initialize GPG
def initialize_gpg():
    global gpg
    homedir = '/home/vagrant/.gnupg'
    try:
        gpg = gnupg.GPG(gnupghome=homedir) 
    except TypeError:
        gpg = gnupg.GPG(homedir=homedir)

def saveflag(recvdata):
    jd = json.loads(recvdata)
#    print(jd['signer'])
#    print(jd['newflag'])
#    print(jd['signature'])

    sign = base64.b64decode(jd['signature']);
    data = jd['signer']+':'+jd['newflag'];

    with open("/home/vagrant/shared/teamone/msg.txt.sig.det", mode='rb') as file: # b is important -> binary
        fileContent = file.read()

#    fileContent = gpg.sign(data, default_key='TeamOne@hank.com', passphrase='qwer1234', clearsign=False)
#    print(data)
#    print(fileContent)
#    verified = gpg.verify(fileContent)
#    verified = gpg.verify_file("/home/vagrant/shared/teamone/msg.txt.sig.det", sig_file="/home/vagrant/shared/teamone/msg.txt")
#    verified = gpg.verify_file("/home/vagrant/shared/teamone/msg.txt", sig_file="/home/vagrant/shared/teamone/msg.txt.sig.det")
    verified = gpg.verify_data("/home/vagrant/shared/teamone/msg.txt.sig.det", data)

    if not verified:
        print("Invalid Update")

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
            saveflag(b''.join(data).decode('utf-8'))
        finally:
            # Close the connection
            connection.close()
            print("closed")

if __name__ == "__main__":
    initialize_gpg()
    try:
#        server()
        saveflag("{\n\"signer\" : \"james010kim\", \"newflag\" : \"thisisnewflag\", \"signature\" : \"owGbwMvMwMHYExWo4SKzcxLjGrUk9tzidL2SipJISX3frMTc1GIDQ4PszFyrkozM4szivNTytJzE9E5GYxYGRg4GWTFFFt6yvNrTTUqrnvJmXoMZxMoE0s7AxSkAE0l6xcGwm6mxmls7LTivL9DI44r2cf+Lr/6aWc+5sNRwb3ULZ0x2xpKrlvqvX1z8tfjvCzlx/Tk6T2xS49wZZCP8rbq81s1aEeqgxWtzQ9jkjFM0j9/iG2kek27f3131UjZugewHEb5X5QEsoR/z/z/N/ZcoyF8Rss5TnfVc2MWA2x+/vfHXsd1Twc9ZUVamLtEYLn7FOfe6rrmEXchtJW8TPps9XjFyrg13XH9Mk95tHpQkqrNk6/4qb/0ZpcY7zizauDD1w8cyd1NrHhFul/DPUp+XCVn19E8N3/Y3PEQs15q9UHDOB1adjZ/PxWWHfTipZnsqe9u+89a1ng4XTjTrP/7dqrNB13+zhUGFlNt1AA==\" }")	# test for verification of newflag
    except KeyboardInterrupt:
        print ("Ctrl_C pressed ... Shutting Down")
