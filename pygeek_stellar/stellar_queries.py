# 3rd party imports
# Local imports
from .utils.stellar import *


def get_account_balances(cli_session):
    """
    This method is used to fetch all the balances from the current CLI session account
    from the Stellar network.
    :param CliSession cli_session: Current CLI session.
    :return: Returns a list containing the account balances structured in the following manner
    : [['token1', amount], ['token2', amount]]
    :rtype: list of (str, str)
    """
    address = get_address_details_from_network(cli_session.account_address)
    if address is None:
        return None

    balances = []
    for balance in address.balances:
        token_code = balance.get('asset_code', 'XLM')
        token_balance = float(balance.get('balance'))
        balances.append([token_code, token_balance])
    return balances


def get_account_payments(cli_session):
    address = get_address_details_from_network(cli_session.account_address)
    if address is None:
        return None

    return address.payments()


def get_account_transactions(cli_session):
    address = get_address_details_from_network(cli_session.account_address)
    if address is None:
        return None

    return address.transactions()
