import gnupg
import random
import sys

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

# Check if the registered githubId
def check_registered(github_id):
    with open("../github_id.list") as file:
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
    key_data = open('../pubkeys/%s.pub' % github_id).read()
    pubkey = gpg.import_keys(key_data)

    # Encrypt the generated random using the imported public key
    encrypted_data = gpg.encrypt(hex(rand), pubkey.fingerprints[0])
    encrypted_string = str(encrypted_data)
    print ("\nEncrypted: \n%s" % encrypted_string) # FIXME - DEBUG
    return encrypted_string

# Main for testing
if __name__ == "__main__":
    # Get an input from the command line
    input_id = str(sys.argv[1]) 
 
    if(check_registered(input_id)):
       if(check_already_registered(input_id)):
           initialize_gpg()
           generate_challenge(input_id)
       else:
           print ("%s is already registered!" % input_id)
    else:
       print ("%s is not registered!" % input_id)
