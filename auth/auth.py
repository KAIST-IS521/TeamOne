import gnupg
import random
import sys
import os
import base64
from os.path import expanduser

# global variable
id_list = []

# Initialize GPG
def initialize_gpg():
    global gpg
    homedir = expanduser("~") + "/.gnupg"
    try:
        gpg = gnupg.GPG(gnupghome=homedir)
    except TypeError:
        gpg = gnupg.GPG(homedir=homedir)

# Check if the registered githubId
def check_registered(github_id):
    if not id_list:
        with open("./db/github_id.list") as file:
             for id in file:
                 id = id.strip()
                 id_list.append(id)
    return github_id in id_list

# Generate a big random number (256-bit)
def generate_random(github_id):
    return random.getrandbits(256)

# Generate a challenge
# Encrypt(random) || Sign(Encrypt(random))
def generate_challenge(github_id, rand, input_passphrase):
    # Import a public key from a certificate file
    key_data = open('./db/pubkeys/%s.pub' % github_id).read()
    pubkey = gpg.import_keys(key_data)

    # Import a public key of server
    my_key_data = open('./server.pub').read()
    my_pubkey = gpg.import_keys(my_key_data)

    # Encrypt the generated random using the imported public key
    encrypted_data = gpg.encrypt(hex(rand), pubkey.fingerprints[0],
                                 default_key=my_pubkey.fingerprints[0],
                                 passphrase=input_passphrase)
    encrypted_string = str(encrypted_data)

    #return encoded_challenge
    return encrypted_string.encode()

# Verify the response from the user
def verify_response(github_id, encrypted_string, input_passphrase):
    decrypted_data = gpg.decrypt(encrypted_string,
                                 passphrase=input_passphrase)

    if(decrypted_data.ok != True):
        print("Failed to decrypt the response!")
        return

    return str(decrypted_data)
