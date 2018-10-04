import os.path
import json
import requests

from stellar_base.keypair import Keypair
from stellar_base.address import Address
from stellar_base.exceptions import AccountNotExistError

from constants import *

config_file_n_accounts = 0

current_account_initialized = False
current_account_name = None
current_account_keypair = None
current_account_private_key = None
current_account_public_key = None


def main():
    print(CLI_BANNER)

    init_current_account()
    if not current_account_initialized:
        return

    global current_account_public_key
    print('Balance: {} XLM'.format(get_balance(current_account_public_key)))

    fund_testnet_account(current_account_public_key)

    print('Balance: {} XLM'.format(get_balance(current_account_public_key)))


def init_current_account():

    if os.path.isfile(DEFAULT_CONFIG_FILE):
        with open(DEFAULT_CONFIG_FILE, 'r') as config_file:
            configs = json.load(config_file)
            print_config_file_accounts(configs)

            n_accounts = len(configs[JSON_ACCOUNTS_TAG])
            set_config_file_n_accounts(n_accounts)

            if input('Do you want to use an existent account? (y/n): ') == 'y':
                account_n = int(input('Which account do you want to use? (specify the index): '), base=10) - 1
                if account_n < 0 or account_n > n_accounts:
                    print("Specified account index is invalid")
                    return

                name = configs[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_NAME_TAG]
                pub_key = configs[JSON_ACCOUNTS_TAG][account_n][JSON_PUBLIC_KEY_TAG]
                priv_key = configs[JSON_ACCOUNTS_TAG][account_n].get(JSON_PRIVATE_KEY_TAG, None)
                keypair = Keypair.from_seed(priv_key) if priv_key is not None else None

                set_current_account(name, keypair, pub_key, priv_key)

            else:
                ask_user_for_new_account()
                update_config_file(configs)

    else:
        print('Configuration file was not found')
        ask_user_for_new_account()
        update_config_file()

    if not current_account_initialized:
        return

    print('')
    print('The following account will be used:')
    print('   Account Name: {}, Public Key: {}'.format(current_account_name, current_account_public_key))


def print_config_file_accounts(configs_json):
    print("The following Stellar accounts were found:")
    for i, account in enumerate(configs_json[JSON_ACCOUNTS_TAG]):
        print('[{}] Account Name: {}, Public Key: {}'.format(
            i+1, account[JSON_ACCOUNT_NAME_TAG], account[JSON_PUBLIC_KEY_TAG]))


def ask_user_for_new_account():
        if input('Do you wish to add a new Stellar account? (y/n): ') != 'y':
            return

        account_name = input('What is the name of the account? If no name is specified a default one will be used: ')
        if account_name == '':
            global config_file_n_accounts
            account_name = str('Account {}').format(config_file_n_accounts + 1)

        keypair = gen_keypair()
        set_current_account(account_name, keypair[0], keypair[1], keypair[2])


def update_config_file(accounts = {JSON_ACCOUNTS_TAG:[]}):
        if not current_account_initialized:
            return

        accounts[JSON_ACCOUNTS_TAG].append({
            JSON_ACCOUNT_NAME_TAG: current_account_name,
            JSON_PUBLIC_KEY_TAG: current_account_public_key,
            JSON_PRIVATE_KEY_TAG: current_account_private_key})

        config_file = open(DEFAULT_CONFIG_FILE, 'w')
        config_file.write(json.dumps(accounts))


def gen_keypair():
    kp = Keypair.random()
    public_key = kp.address().decode()
    private_key = kp.seed().decode()
    return [kp, public_key, private_key]


def set_current_account(name, keypair, pub_k, priv_k):
    global current_account_name, \
        current_account_private_key, \
        current_account_public_key, \
        current_account_keypair, \
        current_account_initialized

    current_account_name = name
    current_account_keypair = keypair
    current_account_private_key = priv_k
    current_account_public_key = pub_k
    current_account_initialized = True


def get_balance(public_key):
    address = Address(address=public_key)
    try:
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
    return address.balances


def fund_testnet_account(address):
    r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + address)
    return r.text

def set_config_file_n_accounts(n_accounts):
            global config_file_n_accounts
            config_file_n_accounts = n_accounts


if __name__ == "__main__":
    main()
