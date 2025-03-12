import os
import hashlib
import secrets
import sys
import base64
from cryptography.fernet import Fernet

GUI_AVAILABLE = False
if "DISPLAY" in os.environ or sys.platform == "win32":
    try:
        import tkinter as tk
        from tkinter import messagebox, simpledialog
        GUI_AVAILABLE = True
    except ImportError:
        pass

FILE_PATH = "test.txt" 
ENCRYPTED_PATH = "minecraft.locked"
SALT_FILE = "salt.bin"

def derive_key(password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
    return base64.urlsafe_b64encode(key)

def encrypt_file(password: str):
    if not os.path.exists(FILE_PATH):
        print("Error: File not found!")
        return
    
    salt = secrets.token_bytes(16)
    derived_key = derive_key(password, salt)
    cipher = Fernet(derived_key)
    
    with open(FILE_PATH, "rb") as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    
    with open(ENCRYPTED_PATH, "wb") as f:
        f.write(encrypted_data)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    
    os.remove(FILE_PATH)
    print("File locked. Use your password to unlock.")

# Decrypt the file
def decrypt_file(password: str):
    if not os.path.exists(ENCRYPTED_PATH) or not os.path.exists(SALT_FILE):
        print("Error: Required files not found!")
        return
    
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
    
    derived_key = derive_key(password, salt)
    cipher = Fernet(derived_key)
    
    try:
        with open(ENCRYPTED_PATH, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    except:
        print("Error: Decryption failed! Invalid password or corrupted file.")
        return
    
    with open(FILE_PATH, "wb") as f:
        f.write(decrypted_data)
    
    os.remove(ENCRYPTED_PATH)
    os.remove(SALT_FILE)
    print("File unlocked successfully.")

def main():
    if GUI_AVAILABLE:
        root = tk.Tk()
        root.withdraw()
        
        action = simpledialog.askstring("Input", "Type 'lock' to encrypt or 'unlock' to decrypt:")
        if action:
            action = action.strip().lower()
            password = simpledialog.askstring("Password", "Enter password:", show='*')
            
            if not password:
                messagebox.showerror("Error", "Password cannot be empty!")
                return
            
            if action == "lock":
                encrypt_file(password)
            elif action == "unlock":
                decrypt_file(password)
            else:
                messagebox.showerror("Error", "Invalid action.")
    else:
        print("Running in CLI mode (GUI not available).")
        action = input("Type 'lock' to encrypt or 'unlock' to decrypt: ").strip().lower()
        password = input("Enter password: ")
        
        if not password:
            print("Error: Password cannot be empty!")
            return
        
        if action == "lock":
            encrypt_file(password)
        elif action == "unlock":
            decrypt_file(password)
        else:
            print("Error: Invalid action.")

if __name__ == "__main__":
    main()