# System imports
import requests
import json
# 3rd party imports
from stellar_base.address import Address
from stellar_base.exceptions import *
# Local imports
from constants import *


def get_xlm_balance(cli_session):
    """
    This method is used to fetch the XLM balance of the current CLI session account
    from the Stellar network.
    :param cli_session: Current CLI session.
    :return: Returns the XLM balance.
    """
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_XLM)


def get_magnet_balance(cli_session):
    """
    This method is used to fetch the Magnet balance of the current CLI session account
    from the Stellar network.
    :param cli_session: Current CLI session.
    :return: Returns the Magnet balance.
    """
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_MAGNET)


def get_asset_balance(cli_session, asset):
    """
    This method is used to fetch the balance from a given asset of the current CLI
    session account from the Stellar network.
    :param cli_session: Current CLI session.
    :param asset: Asset to be evaluated.
    :return: Returns the balance of the given asset.
    """
    address = Address(address=cli_session.public_key)
    try:
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
        return 0
    except HorizonError:
        print("A connection error occurred (Please check your Internet connection)")
        return -1

    for balance in address.balances:
        if balance.get('asset_type') == asset:
            return float(balance.get('balance'))
    return 0


def fund_using_friendbot(cli_session):
    """
    This method is used to request the Stellar Friendbot to fund the current CLI session
    account. This will only work on the Stellar testnet.
    :param cli_session: Current CLI session.
    :return: Returns a string with the result of the fund request.
    """
    try:
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, cli_session.public_key))
        return 'Successful transaction request' if 200 <= r.status_code <= 299 \
            else 'Failed transaction request (Maybe this account was already funded by Friendbot). Status code {}'.\
            format(r.status_code)
    except requests.exceptions.ConnectionError:
        return "A connection error occurred (Please check your Internet connection)"
