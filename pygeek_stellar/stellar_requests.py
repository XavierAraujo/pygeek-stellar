# System imports
import requests
import base64
# 3rd party imports
from stellar_base.address import Address
from stellar_base.exceptions import *
from stellar_base.builder import Builder
from stellar_base.stellarxdr import Xdr
from stellar_base.stellarxdr import StellarXDR_const
from xdrlib import Error as XDRError
# Local imports
from .utils.stellar import *
from .user_input import *
from .constants import *
from .utils.generic import *


def create_new_account(cli_session, account_address, amount, transaction_memo=''):
    """
    This method creates a new Stellar account. For this to be done a certain amount
    of XLM must be transferred the Stellar account.
    :param cli_session: Current CLI session.
    :param account_address: Address of the new account.
    :param amount: XLM amount to transfer to the new account.
    :param transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """
    private_key = _fetch_valid_private_key(cli_session)
    if private_key is None:
        return

    if not is_valid_stellar_public_key(account_address):
        print('The given account address is invalid')
        return

    if yes_or_no_input('To create the new account, a payment of {} XLM will be done '
                       'to the following address {}. Are you sure you want to proceed?'
                       .format(amount, account_address)) == USER_INPUT_NO:
        return

    builder = Builder(secret=private_key)
    builder.add_text_memo(transaction_memo)
    builder.append_create_account_op(
        destination=account_address,
        starting_balance=amount,
        source=cli_session.public_key)
    response = _sign_and_submit_operation(builder)
    #process_server_payment_response(response) # TODO: Parse response


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
        asset_description = balance.get('asset_code', 'XLM')
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
        return 'Successful transaction request' if is_sucessful_http_status_code(r.status_code) \
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

    token_issuer = None
    send_payment(cli_session, destination_address, amount, 'XLM', token_issuer, transaction_memo)


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

    builder = Builder(secret=private_key)
    builder.add_text_memo(transaction_memo)
    builder.append_payment_op(
        destination=destination_address,
        amount=amount,
        asset_issuer=token_issuer,
        asset_code=asset_type)
    response = _sign_and_submit_operation(builder)
    process_server_payment_response(response)


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

    builder = Builder(secret=private_key)
    builder.add_text_memo(transaction_memo)
    builder.append_trust_op(
        destination=destination_address,
        code=token_code,
        limit=token_limit)
    response = _sign_and_submit_operation(builder)
    process_server_payment_response(response)


def _sign_and_submit_operation(builder):
    builder.sign()
    try:
        return builder.submit()
    except Exception as e:
        # Too broad exception because no specific exception is being thrown by the stellar_base package.
        # TODO: This should be fixed in future versions
        print("An error occurred (Please check your Internet connection)")
        return None


def process_server_payment_response(response):
    if response is None:
        return

    if response.get('status') is not None:
        print("Server response status code: {}".format(response.get('status')))
    if response.get('title') is not None:
        print("Server response title: {}".format(response.get('title')))
    if response.get('detail') is not None:
        print("Server response detail: {}".format(response.get('detail')))
    if 'extras' in response and 'result_xdr' in response['extras']:
        unpacked_tx_result = decode_xdr_transaction_result(response['extras']['result_xdr'])
        print_xdr_transaction_result(unpacked_tx_result)
    if 'result_xdr' in response:
        unpacked_tx_result = decode_xdr_transaction_result(response.get('result_xdr'))
        print_xdr_transaction_result(unpacked_tx_result)


def decode_xdr_transaction_result(xdr_string):
    try:
        xdr_bytes = base64.b64decode(xdr_string)
        return Xdr.StellarXDRUnpacker(xdr_bytes).unpack_TransactionResult()
    except TypeError or ValueError:
        print("Error during base64 decoding")
        return None
    except XDRError:
        print("Error during XDR unpacking procedure")
        return None


def print_xdr_transaction_result(unpacked_tx_result):
        payment_result = unpacked_tx_result.result.results[0].paymentResult
        print("Server response operation result: {}".format(
            'Succeeded' if unpacked_tx_result.result.code == StellarXDR_const.txSUCCESS else 'Failed'))
        print('Server response payment result: {} (Code: {})'.format(str(payment_result), payment_result.code))


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
