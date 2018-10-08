# System imports
import requests
# 3rd party imports
from stellar_base.address import Address
from stellar_base.exceptions import *
from stellar_base.builder import Builder
# Local imports
from .utils.stellar import *
from .user_input import *
from .constants import *


def get_account_balances(cli_session):
    """
    This method is used to fetch all the balances from the current CLI session account
    from the Stellar network.
    :param cli_session: Current CLI session.
    :return: Returns a list containing the account balances structured in the following manner
    : [['asset1', amount], ['asset2', amount]]
    """
    address = _get_address_from_public_key(cli_session.public_key)

    if address is None:
        return None

    balances = []
    for balance in address.balances:
        asset_description = 'XLM' if balance.get('asset_type') == 'native' else balance.get('asset_code')
        asset_balance = float(balance.get('balance'))
        balances.append([asset_description, asset_balance])
    return balances


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


def send_token_payment(cli_session, destination_address, token_name, amount, token_issuer, transaction_memo=''):
    """
    This method is used to send a transaction of the specified token to a given address.
    :param cli_session: Current CLI session.
    :param destination_address: Destination address (equivalent to the public key).
    :param token_name: Name of the token.
    :param amount: Amount of tokens to send.
    :param token_issuer: Issuer of the token to be sent.
    :param transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """

    send_payment(cli_session, destination_address, amount, token_name, token_issuer, transaction_memo)


def send_payment(cli_session, destination_address, amount, asset_type, token_issuer=None, transaction_memo=''):
    """
    This method is used to send a transaction of the specified asset type to a given address.
    :param cli_session: Current CLI session.
    :param destination_address: Destination address (equivalent to the public key).
    :param amount: Amount to be sent.
    :param asset_type: Asset type to be sent.
    :param token_issuer: Issuer of the token to be sent. It can be None when dealing with native asset (XLM).
    :param transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """

    private_key = _fetch_valid_private_key(cli_session)
    if private_key is None:
        return

    if not is_valid_stellar_public_key(destination_address):
        print('The given destination address is invalid')
        return
    if destination_address == cli_session.public_key:
        print('Sending payment to own address. This is not allowed')
        return
    if token_issuer is not None and not is_valid_stellar_public_key(token_issuer):
        print('The given token issuer address is invalid')
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
            asset_issuer=token_issuer,
            asset_code=asset_type)
        builder.sign()
        response = builder.submit()
        print(response)
    except Exception as e:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")


def establish_trustline(cli_session, destination_address, token_code, token_limit, transaction_memo=''):
    private_key = _fetch_valid_private_key(cli_session)
    if private_key is None:
        return

    if not is_valid_stellar_public_key(destination_address):
        print('The given destination address is invalid')
        return
    if destination_address == cli_session.public_key:
        print('Sending change of trust transaction to own address. This is not allowed')
        return
    if not is_valid_stellar_transaction_text_memo(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    try:
        builder = Builder(secret=private_key)
        builder.add_text_memo(transaction_memo)
        builder.append_trust_op(destination_address, token_code, token_limit)
        builder.sign()
        response = builder.submit()
        print(response)
    except Exception as e:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")


def _fetch_valid_private_key(cli_session):
    private_key = cli_session.private_key
    if private_key is None \
            or not is_valid_stellar_private_key(private_key) \
            or not is_priv_key_matching_pub_key(private_key, cli_session.public_key):
        private_key = _ask_user_for_private_key(cli_session,
                                                "Either no private key was found for this CLI session account, "
                                                "the private key for this CLI session account is invalid or "
                                                "the private key does match the current CLI session account public "
                                                "key. No transaction can be made without a valid private key. Please "
                                                "insert your private key to process the transaction")
    return private_key


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


def _get_address_from_public_key(public_key):
    try:
        address = Address(address=public_key)
        address.get()  # Get the latest information from Horizon
    except AccountNotExistError:
        print('The specified account does not exist')
        return None
    except HorizonError:
        print('A connection error occurred (Please check your Internet connection)')
        return None
    return address
