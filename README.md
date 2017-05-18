# TeamOne Bank
We are providing a virtual banking system based on `python`,`MySQL`, and `GnuPG`.
To use this system, customers need their GitHub ID and PGP key for user registration.
After user registration, the customers can transfer money to other customers freely.
As an opening event, the customers will earn 1,000 won after the initial registrations.

## Menu

### Entry Menu
1. **Login**
   * The customer can access the banking system via ID/Password Login.
   * ID/Password is created when the customer is registered.
2. **Register**
   * To create an account, the customer needs to register the banking system.
   * For this, the customer inputs GitHub ID and receives the encrypted challenge from the banking system.
   * Using the BASE64-encoded challenge, the customer generates the encrypted response for PGP authentication.
   * After the PGP authentication succeeds, the customer can create his/her account by entering ID, Password, e-mail, and cellphone number.
3. **Terminate**
   * The customer can exit this banking system.

### Main Menu
1. **Check balance**: Display th current balance of the customer
2. **Check transaction history**: Display the transaction records
3. **Transfer**: Send money to other customers
4. **Edit user info**: Edit the detail user information or remove the user account

## How to Use

### Build the system
```
~/TeamOne$ make
```

## How to launch the banking server
```
~/TeamOne$ cd server
~/TEamOne/server$  python3 main.py passphrase
```

## How to access the banking system
```
> nc ip_addr 1588
``` 
