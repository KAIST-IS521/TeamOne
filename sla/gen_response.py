import sys, os, base64
import gnupg

# Initialize GPG
def initialize_gpg():
    global gpg
    homedir = '/home/vagrant/.gnupg'
    try:
        gpg = gnupg.GPG(gnupghome=homedir)
    except TypeError:
        gpg = gnupg.GPG(homedir=homedir)

# Split the challenge
def split_challenge(decoded_challenge):
    challenge = decoded_challenge.split(b'-----BEGIN PGP PUBLIC KEY BLOCK-----')

    challenge[1] = b'-----BEGIN PGP PUBLIC KEY BLOCK-----' + challenge[1]

    return challenge

# Main
if __name__ == "__main__":
    input_passphrase = str(sys.argv[1])
    encoded_challenge = str(sys.argv[2])

    initialize_gpg()

    # Decode base64
    decoded_challenge = base64.b64decode(encoded_challenge)
    
    # Split decoded challenge into encerypted random and server's pubkey
    challenge = split_challenge(decoded_challenge)

    # Decrypt the encrypted random using my private key
    decrypted_data = gpg.decrypt(challenge[0], passphrase=input_passphrase)

    if (decrypted_data.ok != True):
        print ("Decryption failed...")
    else:
        # Use server's pubkey for encryption
        pubkey = gpg.import_keys(challenge[1])
    
        # Encrypt the decrypted random using server's pubkey
        encrypted_data = gpg.encrypt(str(decrypted_data), pubkey.fingerprints[0])
        encrypted_string = str(encrypted_data)

        # Print-out the result
        print ("\nEncrypted response:\n")
        encoded_response = base64.b64encode(encrypted_string.encode())
        print (str(encoded_response.decode()))
