
from cli_session import *
from stellar_account import *

def main():
    print(CLI_BANNER)

    cli_session = init_cli_session()
    if not cli_session:
        return
    print_current_session_account(cli_session)

    account = StellarAccount(cli_session)

    result = account.fund_using_friendbot()
    #print('Friendbot funding result: ' + result)
    print('Balance: {} XLM'.format(account.get_balance()))


def print_current_session_account(cli_session):
    print('')
    print('The following account will be used: {}'.format(cli_session.to_str()))
    print('')





if __name__ == "__main__":
    main()
