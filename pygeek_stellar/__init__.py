# System imports
from geek_stellar_cmd import GeekStellarCmd
# Local imports
from cli_session import *


def main():
    print(CLI_BANNER)

    session = cli_session_init()
    if not session:
        return

    cmd = GeekStellarCmd(session)
    cmd.do_cls(None)
    print_current_session_account(session)
    cmd.do_help(None)
    cmd.cmdloop()


def print_current_session_account(session):
    print('\nThe following account was chosen: {}\n'.format(session.to_str()))


if __name__ == "__main__":
    main()
