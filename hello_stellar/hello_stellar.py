import argparse

from cli_session import *
from stellar_account import *


def main():
    print(CLI_BANNER)

    cli_session = init_cli_session()
    if not cli_session:
        return
    print_current_session_account(cli_session)

    account = StellarAccount(cli_session)
    configure_cmd_input_parser(account)


def configure_cmd_input_parser(stellar_account):
    parser = argparse.ArgumentParser()

    parser.add_argument('-xlm', action='store_true',
                        help='Displays the current XLM balance of the selected account')
    parser.add_argument('-mag', action='store_true',
                        help='Displays the current Magnet balance of the selected account')
    parser.add_argument('-fund', action='store_true',
                        help='Asks the Stellar test-net Friendbot to send XLM to the selected account')

    args = parser.parse_args()

    if args.xlm:
        print_xlm_balance(stellar_account)
    if args.mag:
        print_magnet_balance(stellar_account)
    if args.fund:
        request_friendbot_funds(stellar_account)


def print_xlm_balance(stellar_account):
    print('XLM Balance: {}'.format(stellar_account.get_xlm_balance()))


def print_magnet_balance(stellar_account):
    print('Magnet Balance: {}'.format(stellar_account.get_magnet_balance()))


def request_friendbot_funds(stellar_account):
    result = stellar_account.fund_using_friendbot()
    print('Friendbot funding result: ' + result)


def print_current_session_account(cli_session):
    print('')
    print('The following account will be used: {}'.format(cli_session.to_str()))
    print('')


if __name__ == "__main__":
    main()
