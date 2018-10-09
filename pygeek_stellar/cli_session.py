# 3rd party imports
from stellar_base.keypair import Keypair
# Local imports
from .constants import *
from .utils.user_input import *
from .utils.file import *
from .utils.generic import *


class CliSession:
    """
    
    Attributes
    ----------
    configs : json
        Content of the configuration file
    account_name : str
        Name of the Stellar account used on the CLI session
    account_address : str
        Address of the Stellar account used on the CLI session
    account_seed : str
        Secret seed of the Stellar account used on the CLI session. The seed
        is a string that can be used to decode both private and public key of the account
    """

    def __init__(self, configs, account_name, account_address, account_seed):

        self.configs = configs
        self.account_name: str = account_name
        self.account_address: str = account_address
        self.account_seed: str = account_seed

    def update_config_file(self, file):

        if self.configs is None:
            self.configs = {JSON_ACCOUNTS_TAG: []}  # Init with empty accounts

        self.configs[JSON_ACCOUNTS_TAG].append({
            JSON_ACCOUNT_NAME_TAG: self.account_name,
            JSON_ACCOUNT_ADDRESS_TAG: self.account_address,
            JSON_ACCOUNT_SEED_TAG: self.account_seed})

        config_file = open(file, 'w')
        succeeded = config_file.write(json.dumps(self.configs))
        if succeeded:
            print("Saved configuration file in: {}".format(file))

    def to_str(self):
        return 'Account Name: {}, Account Address: {}'.format(self.account_name, self.account_address)


def cli_session_init():
    n_accounts_found = 0
    configs = None
    file_content = load_file(DEFAULT_CONFIG_FILE)
    if file_content is not None:
        configs = decode_json_content(file_content)

    if configs is not None:
        n_accounts_found = len(configs[JSON_ACCOUNTS_TAG])
        _print_config_file_accounts(configs)

    if n_accounts_found > 0:
        if yes_or_no_input('Do you want to use an existent account?') == USER_INPUT_YES:
            account_n = int_input('Which account do you want to use? (specify the index)') - 1
            if account_n < 0 or account_n > n_accounts_found:
                print("Specified account index is invalid")
                return None

            name = configs[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_NAME_TAG]
            address = configs[JSON_ACCOUNTS_TAG][account_n][JSON_ACCOUNT_ADDRESS_TAG]
            seed = configs[JSON_ACCOUNTS_TAG][account_n].get(JSON_ACCOUNT_SEED_TAG, None)
            return CliSession(configs, name, address, seed)

    if yes_or_no_input('Do you wish to add a new Stellar account?') == USER_INPUT_NO:
        return None

    account_name = safe_input('What is the name of the account? (If no name is specified a default one will be used)')
    if account_name == '':
        account_name = str('Account {}').format(n_accounts_found + 1)

    keypair = Keypair.random()
    cli_session = CliSession(configs, account_name, keypair.address().decode(), keypair.seed().decode())
    cli_session.update_config_file(DEFAULT_CONFIG_FILE)
    return cli_session


def _print_config_file_accounts(configs_json):
    print('The following {} Stellar accounts were found on the configuration file:'.format(
        len(configs_json[JSON_ACCOUNTS_TAG])))
    for i, account in enumerate(configs_json[JSON_ACCOUNTS_TAG]):
        print('[{}] Account Name: {}, Account Address: {}'.format(
            i+1, account[JSON_ACCOUNT_NAME_TAG], account[JSON_ACCOUNT_ADDRESS_TAG]))
    print('')
