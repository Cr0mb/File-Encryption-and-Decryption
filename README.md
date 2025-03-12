# File-Encryption-and-Decryption
This Python script allows you to encrypt and decrypt a file using a password. The file is encrypted using the cryptography library, and the password is used to derive a cryptographic key using the PBKDF2-HMAC-SHA256 algorithm. The encrypted file is saved with a .locked extension, and a salt file is used to securely derive the key for decryption.


The script can run either in CLI mode or with a GUI (using tkinter).

## Features
1. File Encryption: Encrypts a file using a password to generate a unique key.
2. File Decryption: Decrypts the encrypted file using the correct password.
3. Password-based Security: Passwords are used to derive a cryptographic key via PBKDF2-HMAC.
4. CLI and GUI Modes: Choose to run in a simple command-line interface or use a graphical user interface with tkinter (if available).

## Requirements
To run this script, you need the following libraries:
- Python 3.x
```
pip install cryptography tkinter
```

