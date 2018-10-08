# 3rd party imports
import stellar_base.utils
from stellar_base.exceptions import *
from stellar_base.keypair import Keypair

STELLAR_MEMO_TEXT_MAX_BYTES = 28


def is_valid_stellar_public_key(key):
    if key is None:
        return False
    try:
        stellar_base.utils.decode_check('account', key)
        return True
    except DecodeError:
        return False


def is_valid_stellar_private_key(key):
    if key is None:
        return False
    try:
        stellar_base.utils.decode_check('seed', key)
        return True
    except DecodeError:
        return False


def is_valid_stellar_transaction_text_memo(memo):
    return False if len(memo) > STELLAR_MEMO_TEXT_MAX_BYTES else True


def is_priv_key_matching_pub_key(private_key, public_key):
    if not is_valid_stellar_private_key(private_key) \
            or not is_valid_stellar_public_key(public_key):
        return False

    keypair = Keypair.from_seed(seed=private_key)
    if keypair.address().decode() == public_key:
        return True
    return False
