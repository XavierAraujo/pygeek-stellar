import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken


def encrypt(content, password):
    """
    Method to encrypt the given content based on the specified password
    :param content: Content to be encrypted. It must be a byte array
    :param password: Encryption password
    :return: Returns a byte array with the encrypted content
    """
    f = Fernet(password2cryptographic_key(password))
    return f.encrypt(content)


def decrypt(content, password):
    """
    Method to decrypt the given content based on the specified password
    :param content: Content to be decrypted. It must be a byte array
    :param password: Decryption password
    :return: Returns a byte array with the decrypted content
    """

    f = Fernet(password2cryptographic_key(password))
    try:
        decrypted_content = f.decrypt(content)
    except InvalidToken:
        print("The file could not be decrypted. Please check if the password is correct")
        return None
    return decrypted_content


def password2cryptographic_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bytes("0"*16, 'utf-8'),  # os.urandom(16) TODO: Check salt influence
        iterations=100000,
        backend=default_backend())

    key = kdf.derive(password.encode())  # derive key from the user password
    return base64.urlsafe_b64encode(key)
