# 3rd party imports
import stellar_base.utils
from stellar_base.exceptions import *
from stellar_base.keypair import Keypair

STELLAR_MEMO_TEXT_MAX_BYTES = 28


def is_valid_public_key(key):
    """
    Checks if a given Stellar public key/address is valid.
    :param key: Public key/address to be evaluated.
    :type key: str
    :return: Returns true if the given public key/address is valid and false otherwise.
    :rtype: bool
    """
    if key is None:
        return False
    try:
        stellar_base.utils.decode_check('account', key)
        return True
    except DecodeError:
        return False


def is_valid_private_key(key):
    """
    Checks if a given Stellar private key/seed is valid.
    :param key: Private key/seed to be evaluated.
    :type key: str
    :return: Returns true if the given private key/seed is valid and false otherwise.
    :rtype: bool
    """
    if key is None:
        return False
    try:
        stellar_base.utils.decode_check('seed', key)
        return True
    except DecodeError:
        return False


def is_valid_transaction_text_memo(memo):
    """
    Checks if a given Stellar transaction text memo is valid. To be valid the memo
    can only have, at most, 28 bytes.
    :param memo: Text memo to be evaluated.
    :type memo: str
    :return: Returns true if the given text memo is valid and false otherwise.
    :rtype: bool
    """
    return False if len(memo) > STELLAR_MEMO_TEXT_MAX_BYTES else True


def is_valid_keypair(private_key, public_key):
    """
    Checks if the specified private key/seed matches the specified public key/address.
    If the keys match it means that they form a Stellar keypair.
    :param private_key: Private key/seed to be evaluated.
    :type private_key: str
    :param public_key: Public key/address to be evaluated.
    :type public_key: str
    :return: Returns true if the given keys form a keypair and false otherwise.
    :rtype: bool
    """
    if not is_valid_private_key(private_key) \
            or not is_valid_public_key(public_key):
        return False

    keypair = Keypair.from_seed(seed=private_key)
    if keypair.address().decode() == public_key:
        return True
    return False
