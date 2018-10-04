import os.path
import json
from stellar_base.keypair import Keypair
from constants import *
import user_input

class CliSession:

    def __init__(self, configs, account_name, keypair, public_key, private_key):
        self.configs = configs
        self.account_name: str = account_name
        self.keypair: Keypair = keypair
        self.public_key: str = public_key
        self.private_key: str = private_key

    def update_config_file(self):

        if self.configs is None:
            self.configs = {JSON_ACCOUNTS_TAG: []}

        self.configs[JSON_ACCOUNTS_TAG].append({
            JSON_ACCOUNT_NAME_TAG: self.account_name,
            JSON_PUBLIC_KEY_TAG: self.public_key,
            JSON_PRIVATE_KEY_TAG: self.private_key})

        config_file = open(DEFAULT_CONFIG_FILE, 'w')
        config_file.write(json.dumps(self.configs))


def init_cli_session():

    configs = _load_config_file_content()

    n_accounts_found = len(configs[JSON_ACCOUNTS_TAG])
    _print_config_file_accounts(configs)

    if n_accounts_found > 0:
        if user_input.yes_or_no_input('Do you want to use an existent account?') == 'y':
            account_n = int(input('Which account do you want to use? (specify the index): '), base=10) - 1
            if account_n < 0 or account_n > n_accounts_found:
                print("Specified account index is invalid")
                return None

            name = configs[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_NAME_TAG]
            pub_key = configs[JSON_ACCOUNTS_TAG][account_n][JSON_PUBLIC_KEY_TAG]
            priv_key = configs[JSON_ACCOUNTS_TAG][account_n].get(JSON_PRIVATE_KEY_TAG, None)
            keypair = Keypair.from_seed(priv_key) if priv_key is not None else None
            return CliSession(configs, name, keypair, pub_key, priv_key)

    if user_input.yes_or_no_input('Do you wish to add a new Stellar account?') != 'y':
        return None

    account_name = input('What is the name of the account? If no name is specified a default one will be used: ')
    if account_name == '':
        account_name = str('Account {}').format(n_accounts_found + 1)

    keypair = Keypair.random()
    cli_session = CliSession(None, account_name, keypair, keypair.address().decode(), keypair.seed().decode())
    cli_session.update_config_file()
    return cli_session


def _print_config_file_accounts(configs_json):
    print('The following {} Stellar accounts were found on the configuration file:'.format(
        len(configs_json[JSON_ACCOUNTS_TAG])))
    for i, account in enumerate(configs_json[JSON_ACCOUNTS_TAG]):
        print('[{}] Account Name: {}, Public Key: {}'.format(
            i+1, account[JSON_ACCOUNT_NAME_TAG], account[JSON_PUBLIC_KEY_TAG]))


def _load_config_file_content():
    if not os.path.isfile(DEFAULT_CONFIG_FILE):
        return {JSON_ACCOUNTS_TAG:[]}  # return empty config file content

    with open(DEFAULT_CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)
