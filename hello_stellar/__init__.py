from cli_session import *
from prompt import Prompt


def main():
    print(CLI_BANNER)

    session = init_cli_session()
    if not session:
        return
    print_current_session_account(session)

    Prompt(session).cmdloop('Starting prompt...')


def print_current_session_account(session):
    print('')
    print('The following account will be used: {}'.format(session.to_str()))
    print('')


if __name__ == "__main__":
    main()
