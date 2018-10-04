import requests
import json
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError


class StellarAccount:

    def __init__(self, cli_session):
        self.cli_session = cli_session

    def get_balance(self):
        address = Address(address=self.cli_session.public_key)
        try:
            address.get()  # Get the latest information from Horizon
        except AccountNotExistError:
            print('The specified account does not exist')
        return address.balances

    def fund_using_friendbot(self):
        r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + self.cli_session.public_key)
        return json.loads(r.text)['title']
