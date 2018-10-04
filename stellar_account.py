import requests
import json
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError
from constants import *


class StellarAccount:

    def __init__(self, cli_session):
        self.cli_session = cli_session

    def get_balance(self):
        address = Address(address=self.cli_session.public_key)
        try:
            address.get()  # Get the latest information from Horizon
        except AccountNotExistError:
            print('The specified account does not exist')
        # return address.balances
        return address.balances[0].get('balance')

    def fund_using_friendbot(self):
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, self.cli_session.public_key))
        return json.loads(r.text)['title']
