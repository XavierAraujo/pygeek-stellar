import stellar_base.utils


def is_float_str(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_valid_stellar_public_key(key):
    try:
        stellar_base.utils.decode_check('account', key)
        return True
    except Exception:
        return False


def is_valid_stellar_private_key(key):
    try:
        stellar_base.utils.decode_check('seed', key)
        return True
    except Exception:
        return False