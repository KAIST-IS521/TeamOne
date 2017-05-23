# Auth

This directory provides `auth` module and `flag updater`.

## `auth.py`
This module provides functions to process the PGP-based user authentication.
This module generates the challenge that encrypts and PGP signs the random number.
Then, this module decrypts the encrypted response from the user.

### How to Use by User
1. Make a file (e.g., `challenge.asc`) by copying and pasting the challenge from the server
   ```
   -----BEGIN PGP MESSAGE-----

   hQEMA40G/F3rFvEuAQf/XCtgX7VqvS67lKS9Y3nIoAyMLPHlc9ez6AsU2AddMpvJ
   WKAxtYpUCo75USKrDH/CjEUoKjVfAWHmRwS+sXroZoornjGyr1jbJOq7+HGDd1eA
   Ljv2zAxFHDC5jo3BDnF06Zts06UDn43XT+JM3I7Bft9zrZsy6dMFAgfkD3UMJ81u
   D8YzI1is/yXLaHbLhvFIGFW4/ML+05rKc3Xf6WWTDCiSw0YURR/3t5FwdVxgEvQ1
   /LneS8Dtbsb7w39E5RAPBmMX1aWl6apgt/c+RS2vVvmC7gtTDhCKZDQ6wH34uU8C
   X+chEYcsz9u3+mt6Z7uXNrJkbPsD7Oav21RR3JAwhNLA7gEh2AmJi+yFYrb7uhB8
   SPD/a8m0YQ448vFcPXV+LSpjrTdWHLOzrkbR016NreJOtla/4XdxhIzh1PInLdF+
   zG/IxSvjGmaEhgOkH/wRnTU8MWryqkg7KFWAWjXxs/UbEKc3bcc+1kvqtdKXm/45
   IySvCFOqh3yWJcFKwpfRSgFxB+fN4EWE8edVbSy4c5TCEVZTIiRdxoXSJ2F8X1IM
   VP6VBH8Bbwr2T3MJtWAeYn9xOInlEH1YG+NFHbTGaj9+w1B43rf1wddqbz6RK6TY
   tPPs3y+YZIi8epX2tNhZOD8MDoQojHdaYwu0baqPpIX4ReJ6le7/bTDEcLihv3gv
   zzd4nEC5Q+ArSR8GQH8UiRrnC24DcrSjjSZKsFwaSfP5c4sFoTx1H8wYl3fJCo9v
   PJBTYprVrlYyY2DlI0fP2R4y39kdQYqxl5Q+I62kxvWP6/0FXCsn3bon5CW3Eutz
   V5ISQTbeBoegTjXg41w/UEFkv1AiNiwLT/80EVR7twHRDU80ZvnKiwkxz85iB28f
   wcY+ZDzGQmsuQsHGq4TrjMGYgyNvEHZ9CadHQ7vvaC4=
   =nxX2
   -----END PGP MESSAGE-----
   ```
2. Decrypt the file and make the output file (e.g., `decrypted.txt`)
   ```
   ~$ gpg --output decrypted.txt --decrypt challenge.asc
   ```
3. Generate the encrypted response and make the output file (e.g., `encrypted.txt.asc`)
   ```
   ~$ gpg --recipient "Happyhacking TeamOne" --output encrypted.txt.asc --armor --encrypt decrypted.txt
   ```

## `flagupdater.py`
A flag updater is standalone program for updating new flag.
If flag updater verifies the signature of the JSON message, updates the email address field of “admin” in bank database with the given flag string.

### How to Run
1. Check your team secret and passphrase. Your team's secret key must locate at /home/vagrant/.gnupg/.
    ```
    ~$ gpg -K
    /home/vagrant/.gnupg/secring.gpg
    --------------------------------
    sec   2048R/3C16E5B3 2017-05-16 [expires: 2019-05-16]
    uid                  Happyhacking TeamOne <TeamOne@bank.com>
    ssb   2048R/9EFDDAF8 2017-05-16
    ```
2. Runs as a daemon listening on port 42. You should run with sudo for using privileged port.
    ```
    ~$ sudo python3 flagupdater.py <passphrase>
    ```
