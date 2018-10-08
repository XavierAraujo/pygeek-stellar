# System imports
import os
# Local imports
from .cryptography import *

FILE_MODE_READ = 'r'
FILE_MODE_READ_BINARY = 'rb'
FILE_MODE_WRITE = 'w'
FILE_MODE_WRITE_BINARY = 'wb'


def write_file(filename, content, write_as_binary=False):
    """
    Writes the given content to the specified file
    :param filename: File to which the content should be written
    :param content: Content to be written
    :param write_as_binary: Flag that specifies if the content must be written in binary form or not.
    This parameter is optional and by default files are not written is binary form.
    """
    opening_mode = FILE_MODE_WRITE if not write_as_binary else FILE_MODE_WRITE_BINARY
    file = open(filename, opening_mode)
    file.write(content)


def load_file(filename, read_as_binary=False):
    """
    Loads the specified file to memory
    :param filename: File to be loaded
    :param read_as_binary: Flag that specifies if the file must be loaded in binary form or not.
    This parameter is optional and by default files are not loaded is binary form.
    """
    if os.path.isfile(filename):
        opening_mode = FILE_MODE_READ if not read_as_binary else FILE_MODE_READ_BINARY
        with open(filename, opening_mode) as file_content:
            return file_content.read()
    return None


def write_encrypted_file(filename, content, password):
    """
    Writes the given content to the specified file and encrypts it with the specified password
    :param filename: File to which the content should be written
    :param content: Content to be written
    :param password: Password to encrypt the file
    """
    if not _is_valid_password(password):
        print('A valid password must be given to decrypt the file')
        return None

    encrypted_content = encrypt(content.encode(), password)
    write_file(filename, encrypted_content, write_as_binary=True)  # Encrypted files are stored as binary


def load_encrypted_file(filename, password, read_as_binary=False):
    """
    Loads the specified file to memory and decrypts it with the specified password
    :param filename: File to be loaded
    :param password: Password to decrypt the file
    :param read_as_binary: Flag that specifies if the file must be loaded in binary form or not.
    This parameter is optional and by default files are not loaded is binary form.
    """
    if not _is_valid_password(password):
        print('A valid password must be given to decrypt the file')
        return None

    file_content = load_file(filename, read_as_binary=True)  # Encrypted files are stored as binary
    decrypted_content = decrypt(file_content, password)
    if decrypted_content is None:
        return None
    return decrypted_content if read_as_binary else decrypted_content.decode()


def _is_valid_password(password):
    if password is None or len(password) == 0:
        return False
    return True
