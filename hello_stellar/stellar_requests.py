# System imports
import requests
import json
# 3rd party imports
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError
# Local imports
from constants import *


def get_xlm_balance(cli_session):
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_XLM)


def get_magnet_balance(cli_session):
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_MAGNET)


def get_asset_balance(cli_session, asset):
    address = Address(address=cli_session.public_key)
    try:
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
        return 0

    for balance in address.balances:
        if balance.get('asset_type') == asset:
            return float(balance.get('balance'))
    return 0


def fund_using_friendbot(cli_session):
    r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, cli_session.public_key))
    return json.loads(r.text)['title']
