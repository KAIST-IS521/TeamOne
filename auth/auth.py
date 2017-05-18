import gnupg
import random
import sys
import os
import base64

# global variable
id_list = []

# Initialize GPG
def initialize_gpg():
    global gpg
    homedir = '/home/vagrant/.gnupg'
    try:
        gpg = gnupg.GPG(gnupghome=homedir) 
    except TypeError:
        gpg = gnupg.GPG(homedir=homedir)

# Check if the registered githubId
def check_registered(github_id):
    with open("../db/github_id.list") as file:
         for id in file:
             id = id.strip()
             id_list.append(id)
    return github_id in id_list

# Check if the requested github_id is already registered
def check_already_registered(github_id):
    # TODO - Access DB for this check routine
    return True

# Generate a big random number (256-bit)
def generate_random(github_id):
    return random.getrandbits(256)

# Generate a challenge (encrypted random)
def generate_challenge(github_id, rand):
    # Import a public key from a certificate file
    if __name__ == "__main__": # FIXME - TEST
        key_data = open('./server.pub').read()
    else:
        key_data = open('../db/pubkeys/%s.pub' % github_id).read()

    pubkey = gpg.import_keys(key_data)

    # Encrypt the generated random using the imported public key
    encrypted_data = gpg.encrypt(hex(rand), pubkey.fingerprints[0])
    encrypted_string = str(encrypted_data)

    # Import a server's public key for sending
    my_key_data = open('../server.pub').read()

    # Form the return string
    challenge = encrypted_string + my_key_data
    encoded_challenge = base64.b64encode(challenge.encode())

    return encoded_challenge

# Verify the response from the user
def verify_response(github_id, encrypted_string, input_passphrase):
    decrypted_data = gpg.decrypt(encrypted_string, passphrase=input_passphrase)

    if(decrypted_data.ok != True):
        return  
     
    return str(decrypted_data)   

# Split the challenge (For testing)
def split_challenge(decoded_challenge):
    challenge = decoded_challenge.split(b'-----BEGIN PGP PUBLIC KEY BLOCK-----')
    
    challenge[1] = b'-----BEGIN PGP PUBLIC KEY BLOCK-----' + challenge[1]

    return challenge
