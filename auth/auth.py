import gnupg
import random
import sys
import os

from pprint import pprint

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
# Generate a server key
def generate_server_key():
    if not os.path.exists('./teamone.pub'):
        input_data = gpg.gen_key_input(
        key_type='RSA',
        key_length=2048,
        name_real='TeamOne',
        name_email='teamone@teamone.com',
        passphrase='teamone')
 
        # Generate a GPG key
        key = gpg.gen_key(input_data)
        # Export the key pair
        ascii_armored_public_keys = gpg.export_keys(key)

        # Write the exported public key to a file
        with open('./teamone.pub', 'w') as f:
            f.write(ascii_armored_public_keys)
    else:
        print ("Server key is already generated.")

# Check if the registered githubId
def check_registered(github_id):
    with open("./github_id.list") as file:
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
    print ("Generate a random number for %s" %  github_id)
    return random.getrandbits(256)

# Generate a challenge (encrypted random)
def generate_challenge(github_id):
    # Generate a random number for a given githubId
    rand = generate_random(github_id)
    print ("%s" % hex(rand)) # FIXME - DEBUG
    
    # Import a public key from a certificate file
    if __name__ == "__main__": # FIXME - TEST
        key_data = open('./teamone.pub').read()
    else:
        key_data = open('./pubkeys/%s.pub' % github_id).read()

    pubkey = gpg.import_keys(key_data)

    # Encrypt the generated random using the imported public key
    encrypted_data = gpg.encrypt(hex(rand), pubkey.fingerprints[0])
    encrypted_string = str(encrypted_data)
    print ("\nEncrypted: \n%s" % encrypted_string) # FIXME - DEBUG
    return encrypted_string

# Verify the response from the user
def verify_response(github_id, encrypted_string):
    decrypted_data = gpg.decrypt(encrypted_string, passphrase='teamone')
    
    print ("ok: %s" % decrypted_data.ok)
    print ("decrypted_string: %s" % str(decrypted_data))

    # TODO - check if the decrypted random number is matched with the generated one

# Main for testing
if __name__ == "__main__":
    # Get an input from the command line
    input_id = str(sys.argv[1]) 

    # Initialize GPG & generate a server key 
    initialize_gpg()
    generate_server_key()

    if(check_registered(input_id)):
       if(check_already_registered(input_id)):
           verify_response(input_id, generate_challenge(input_id))
       else:
           print ("%s is already registered!" % input_id)
    else:
       print ("%s is not registered!" % input_id)
