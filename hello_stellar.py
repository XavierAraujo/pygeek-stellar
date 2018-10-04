import requests
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError
from cli_session import *


def main():
    print(CLI_BANNER)

    session = init_cli_session()
    if not session:
        return

    print('')
    print('The following account will be used:')
    print('   Account Name: {}, Public Key: {}'.format(session.account_name, session.public_key))

    fund_testnet_account(session.public_key)
    print('Balance: {} XLM'.format(get_balance(session.public_key)))


def get_balance(public_key):
    address = Address(address=public_key)
    try:
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
    return address.balances


def fund_testnet_account(address):
    r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + address)
    return r.text


if __name__ == "__main__":
    main()
