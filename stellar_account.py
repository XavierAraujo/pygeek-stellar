import requests
import json
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError
from constants import *


class StellarAccount:

    def __init__(self, cli_session):
        self.cli_session = cli_session

    def get_xlm_balance(self):
        return self.get_asset_balance(STELLAR_ASSET_TYPE_XLM)

    def get_magnet_balance(self):
        return self.get_asset_balance(STELLAR_ASSET_TYPE_MAGNET)

    def get_asset_balance(self, asset):
        address = Address(address=self.cli_session.public_key)
        try:
            address.get()  # Get the latest information from Horizon
        except AccountNotExistError:
            print('The specified account does not exist')
            return 0

        for balance in address.balances:
            if balance.get('asset_type') == asset:
                return float(balance.get('balance'))
        return 0

    def fund_using_friendbot(self):
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, self.cli_session.public_key))
        return json.loads(r.text)['title']
