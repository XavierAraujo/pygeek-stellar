# System imports
from cmd import Cmd
import os
import shlex
# Local imports
from .stellar_requests import *
from .stellar_queries import *
from .utils.generic import *


class GeekStellarCmd(Cmd):

    def __init__(self, session):
        super(GeekStellarCmd, self).__init__()
        self.session = session
        self.prompt = '> '

    def cmdloop(self, intro=None):
        """
        Extend the base class cmdloop method to call do_quit() when a KeyboardInterrupt
        (ctr+c) is received
        """
        while True:
            try:
                super(GeekStellarCmd, self).cmdloop()
            except KeyboardInterrupt:
                self.do_quit(None)

    def do_current_account(self, args):
        """
        Prints information regarding the current Stellar account being used
        """
        print('{}'.format(self.session.to_str()))

    def do_get_account_balances(self, args):
        """
        Requests the current XLM (Stellar Lumens) balance from the Stellar Horizon server.
        """
        balances = get_account_balances(self.session)
        if balances is None:
            print('No balances could be retrieved')
            return
        for balance in balances:
            print('  {}: {}'.format(balance[0], balance[1]))

    def do_get_account_payments(self, args):
        """
        Requests info regarding payments from the Stellar Horizon server.
        """
        payments = get_account_payments(self.session)
        if payments is None:
            print('No payments could be retrieved')
            return
        print(payments)
        # TODO: Process payments json

    def do_get_account_transactions(self, args):
        """
        Requests info regarding payments from the Stellar Horizon server.
        """
        transactions = get_account_transactions(self.session)
        if transactions is None:
            print('No transactions could be retrieved')
            return
        print(transactions)
        # TODO: Process transactions json

    def do_request_funds(self, args):
        """
        Requests funds from the Stellar Testnet Friendbot. This request will only be successful
        a single time for each Stellar Testnet address. The request will fail if the address
        belongs to the real Stellar network.
        """
        result = fund_using_friendbot(self.session)
        print('Friendbot funding result: ' + result)

    def do_send_donation(self, args):
        """
        Sends a XLM donation as a form of contribution to the development of pygeek-stellar
        Usage: send_donation {amount} {transaction_memo: optional}
        """
        args = shlex.split(args)
        if len(args) < 1:
            print('A XLM amount is mandatory')
            return

        amount = args[0].replace(',', '.')
        memo = '' if len(args) < 2 else args[1]  # memo is optional

        if not is_float_str(amount):
            print('The transfer amount to transfer must but a valid value')
            return

        send_payment(self.session, STELLAR_DONATION_ADDRESS, 'XLM', amount, None, memo)

    def do_create_new_account(self, args):
        """
        Creates a new Stellar address by transferring a given amount of XLM to that address.
        Usage: create_new_account {account_address} {amount} {transaction_memo: optional}
        """
        args = shlex.split(args)
        if len(args) < 2:
            print('An account address and a transfer amount are mandatory')
            return

        address = args[0]
        amount = args[1].replace(',', '.')
        memo = '' if len(args) < 3 else args[2]  # memo is optional

        if not is_float_str(amount):
            print('The transfer amount to transfer must but a valid value')
            return
        
        create_new_account(self.session, address, amount, memo)
        
    def do_send_token_payment(self, args):
        """
        Sends a XLM payment to the given destination address
        Usage: send_xlm_payment {destination_address} {token_name} {amount} {transaction_memo: optional}
        """
        args = shlex.split(args)
        if len(args) < 3:
            print('A destination address, token name and a transfer amount are mandatory')
            return

        destination = args[0]
        token_name = args[1]
        amount = args[2].replace(',', '.')
        memo = '' if len(args) < 4 else args[3]  # memo is optional

        if not is_float_str(amount):
            print('The transfer amount to transfer must but a valid value')
            return

        # TODO: Check who should be the issuer! Should it be a input from the user?
        send_payment(self.session, destination, token_name, amount, self.session.account_address, memo)

    def do_send_xlm_payment(self, args):
        """
        Sends a XLM payment to the given destination address
        Usage: send_xlm_payment {destination_address} {amount} {transaction_memo: optional}
        """
        args = shlex.split(args)
        if len(args) < 2:
            print('A destination address and a transfer amount are mandatory')
            return

        destination = args[0]
        amount = args[1].replace(',', '.')
        memo = '' if len(args) < 3 else args[2]  # memo is optional

        if not is_float_str(amount):
            print('The transfer amount to transfer must but a valid value')
            return

        send_payment(self.session, destination, 'XLM', amount, None, memo)

    def do_establish_trustline(self, args):
        """
        Creates a new Stellar token with the given name and limit
        Usage: establish_trustline {destination_address} {token_name} {token_limit}
        """
        args = shlex.split(args)
        if len(args) < 3:
            print('A destination address, token name and token limit are mandatory')
            return

        destination = args[0]
        token_name = args[1]
        token_limit = args[2]

        if not is_int_str(token_limit):
            print('The token limit must but a valid integer value')
            return

        establish_trustline(self.session, destination, token_name, token_limit)

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

