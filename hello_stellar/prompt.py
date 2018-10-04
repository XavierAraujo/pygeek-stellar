from cmd import Cmd
from stellar_requests import *


class Prompt(Cmd):

    def __init__(self, session):
        super(Prompt, self).__init__()
        self.session = session
        self.prompt = '> '

    def do_print_xlm_balance(self, args):
        print('XLM Balance: {}'.format(get_xlm_balance(self.session)))

    def do_print_magnet_balance(self, args):
        print('Magnet Balance: {}'.format(get_magnet_balance(self.session)))

    def do_request_friendbot_funds(self, args):
        result = fund_using_friendbot(self.session)
        print('Friendbot funding result: ' + result)