from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt(data: str):
    return cipher.encrypt(data.encode()).decode()

def decrypt(data: str):
    return cipher.decrypt(data.encode()).decode()