# System imports
from cmd import Cmd
import os
# Local imports
from stellar_requests import *


class Prompt(Cmd):

    def __init__(self, session):
        super(Prompt, self).__init__()
        self.session = session
        self.prompt = '> '
        self.completekey = 'tab'

    def do_xlm_balance(self, args):
        """
        Requests the current XLM (Stellar Lumens) balance from the Stellar Horizon server.
        """
        print('XLM Balance: {}'.format(get_xlm_balance(self.session)))

    def do_magnet_balance(self, args):
        """
        Requests the current MAG (Magnets) balance from the Stellar Horizon server.
        """
        print('Magnet Balance: {}'.format(get_magnet_balance(self.session)))

    def do_request_funds(self, args):
        """
        Requests funds from the Stellar Testnet Friendbot. This request will only be successful
        a single time for each Stellar Testnet address. The request will fail if the address
        belongs to the real Stellar network.
        """
        result = fund_using_friendbot(self.session)
        print('Friendbot funding result: ' + result)

    @staticmethod
    def do_cls(args):
        """
        Clear the screen
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Use cls for Windows and clear for Unix

    @staticmethod
    def do_quit(args):
        """
        Quits the program.
        """
        print("Quitting.")
        raise SystemExit
