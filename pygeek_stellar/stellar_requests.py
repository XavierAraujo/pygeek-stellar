# System imports
import requests
# 3rd party imports
from stellar_base.address import Address
from stellar_base.exceptions import *
from stellar_base.builder import Builder
# Local imports
from .utils import *
from .user_input import *


def get_xlm_balance(cli_session):
    """
    This method is used to fetch the XLM balance of the current CLI session account
    from the Stellar network.
    :param cli_session: Current CLI session.
    :return: Returns the XLM balance.
    """
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_XLM)


def get_magnet_balance(cli_session):
    """
    This method is used to fetch the Magnet balance of the current CLI session account
    from the Stellar network.
    :param cli_session: Current CLI session.
    :return: Returns the Magnet balance.
    """
    return get_asset_balance(cli_session, STELLAR_ASSET_TYPE_MAGNET)


def get_asset_balance(cli_session, asset):
    """
    This method is used to fetch the balance from a given asset of the current CLI
    session account from the Stellar network.
    :param cli_session: Current CLI session.
    :param asset: Asset to be evaluated.
    :return: Returns the balance of the given asset.
    """
    address = Address(address=cli_session.public_key)
    try:
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
        return 0
    except HorizonError:
        print("A connection error occurred (Please check your Internet connection)")
        return -1

    for balance in address.balances:
        if balance.get('asset_type') == asset:
            return float(balance.get('balance'))
    return 0


def fund_using_friendbot(cli_session):
    """
    This method is used to request the Stellar Friendbot to fund the current CLI session
    account. This will only work on the Stellar testnet.
    :param cli_session: Current CLI session.
    :return: Returns a string with the result of the fund request.
    """
    try:
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, cli_session.public_key))
        return 'Successful transaction request' if 200 <= r.status_code <= 299 \
            else 'Failed transaction request (Maybe this account was already funded by Friendbot). Status code {}'.\
            format(r.status_code)
    except requests.exceptions.ConnectionError:
        return "A connection error occurred (Please check your Internet connection)"


def send_xlm_payment(cli_session, destination_address, amount, transaction_memo=''):
    """
    This method is used to send a XLM transaction to a given address.
    :param cli_session: Current CLI session.
    :param destination_address: Destination address (equivalent to the public key).
    :param amount: Amount of XLM to send.
    :param transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """

    send_payment(cli_session, destination_address, amount, 'XLM', transaction_memo)


def send_payment(cli_session, destination_address, amount, asset_type, transaction_memo=''):
    """
    This method is used to send a transaction of the specified asset type to a given address.
    :param cli_session: Current CLI session.
    :param destination_address: Destination address (equivalent to the public key).
    :param amount: Amount to be sent.
    :param asset_type: Asset type to be sent.
    :param transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """

    private_key = cli_session.private_key
    if private_key is None \
            or not is_valid_stellar_private_key(private_key)\
            or not is_priv_key_matching_pub_key(private_key, cli_session.public_key):
        private_key = _ask_user_for_private_key(cli_session,
                                                "Either no private key was found for this CLI session account, "
                                                "the private key for this CLI session account is invalid or "
                                                "the private key does match the current CLI session account public "
                                                "key. No transaction can be made without a valid private key. Please "
                                                "insert your private key to process the transaction")
        if private_key is None:
            return

    if not is_valid_stellar_public_key(destination_address):
        print('The given destination address is invalid')
        return
    if destination_address == cli_session.public_key:
        print('Sending payment to own address. This is not allowed')
        return
    if not is_valid_stellar_transaction_text_memo(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    if yes_or_no_input('A payment of {} {} will be done to the following address {}. Are you sure you want to proceed?'
                       .format(amount, asset_type, destination_address)) == USER_INPUT_NO:
        return

    try:
        builder = Builder(secret=private_key)
        builder.add_text_memo(transaction_memo)
        builder.append_payment_op(
            destination=destination_address,
            amount=amount,
            asset_code=asset_type)
        builder.sign()
        response = builder.submit()
        print(response)
    except Exception as e:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")


def _ask_user_for_private_key(cli_session, msg):
    private_key = password_input(msg)
    if not is_valid_stellar_private_key(private_key):
        print('The given private key is invalid')
        return None

    if not is_priv_key_matching_pub_key(private_key, cli_session.public_key):
        print('The given private key does not match with the public key of the current CLI session')
        return None

    if yes_or_no_input('Do you want to save the private key for this CLI session account?') == USER_INPUT_YES:
        cli_session.private_key = private_key

    return private_key
