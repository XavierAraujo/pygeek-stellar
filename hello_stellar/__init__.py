# System imports
from prompt import Prompt
# Local imports
from cli_session import *


def main():
    print(CLI_BANNER)

    session = cli_session_init()
    if not session:
        return

    prompt = Prompt(session)
    prompt.do_cls(None)
    print_current_session_account(session)
    prompt.do_help(None)
    prompt.cmdloop()


def print_current_session_account(session):
    print('')
    print('The following account was chosen: {}'.format(session.to_str()))
    print('')


if __name__ == "__main__":
    main()
