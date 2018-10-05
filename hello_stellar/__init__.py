# System imports
from prompt import Prompt
# Local imports
from cli_session import *


def main():
    print(CLI_BANNER)

    session = cli_session_init()
    if not session:
        return
    print_current_session_account(session)

    prompt = Prompt(session)
    prompt.do_cls(None)
    prompt.do_help(None)
    prompt.cmdloop()


def print_current_session_account(session):
    print('')
    print('The following account will be used: {}'.format(session.to_str()))
    print('')


if __name__ == "__main__":
    main()
