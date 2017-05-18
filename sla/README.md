# SLA

1. `gen_response.py`
    * Generate a client's response to the challenge from the banking server
    * Assume that your private key is already imported in GPG
    * Execute as follows:
      * `passphrase`: passphrase for the private key
      * `encoded_challenge`: the challenge sent from the banking server
    ```
    > python3 gen_response.py passphrase encoded_challange
    ```
