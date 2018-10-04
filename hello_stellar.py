import requests
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError
from cli_session import *


def main():
    print(CLI_BANNER)

    cli_session = init_cli_session()
    if not cli_session:
        return
    print_current_session_account(cli_session)

    fund_testnet_account(cli_session.public_key)
    print('Balance: {} XLM'.format(get_balance(cli_session.public_key)))


def print_current_session_account(cli_session):
    print('')
    print('The following account will be used: {}'.format(cli_session.to_str()))
    print('')


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
