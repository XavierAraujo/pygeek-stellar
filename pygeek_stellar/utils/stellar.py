# 3rd party imports
import stellar_base.utils
from stellar_base.exceptions import *
from stellar_base.keypair import Keypair

STELLAR_MEMO_TEXT_MAX_BYTES = 28


def is_valid_address(address):
    """
    Checks if a given Stellar address is valid. It does not check if it exists on the Stellar
    network, only if it is correctly formatted.
    :param address: address to be evaluated.
    :type address: str
    :return: Returns true if the given address is valid and false otherwise.
    :rtype: bool
    """
    if address is None:
        return False
    try:
        stellar_base.utils.decode_check('account', address)
        return True
    except DecodeError:
        return False


def is_valid_seed(key):
    """
    Checks if a given Stellar seed is valid.
    :param key: Seed to be evaluated.
    :type key: str
    :return: Returns true if the seed is valid and false otherwise.
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
    Checks if a given Stellar transaction text memo is valid. To be valid the text memo
    can only have, at most, 28 bytes.
    :param memo: Text memo to be evaluated.
    :type memo: str
    :return: Returns true if the given text memo is valid and false otherwise.
    :rtype: bool
    """
    if memo is None:
        return False
    return False if len(memo) > STELLAR_MEMO_TEXT_MAX_BYTES else True


def is_address_matching_seed(seed, address):
    """
    Checks if the specified seed address matches the specified address.
    :param seed: Seed to be evaluated.
    :type seed: str
    :param address: Address to be evaluated.
    :type address: str
    :return: Returns true if seed address matches the specified address, and false otherwise.
    :rtype: bool
    """
    if not is_valid_seed(seed) \
            or not is_valid_address(address):
        return False

    keypair = Keypair.from_seed(seed=seed)
    if keypair.address().decode() == address:
        return True
    return False
