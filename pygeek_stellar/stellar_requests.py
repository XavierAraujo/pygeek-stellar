# System imports
import requests
import base64
# 3rd party importsc
from stellar_base.builder import Builder
from stellar_base.stellarxdr import Xdr
from stellar_base.stellarxdr import StellarXDR_const
from xdrlib import Error as XDRError
# Local imports
from .utils.stellar import *
from .utils.user_input import *
from .constants import *
from .utils.generic import *
from .cli_session import CliSession


def create_new_account(cli_session, account_address, amount, transaction_memo=''):
    """
    This method creates a new Stellar account. For this to be done a certain amount
    of XLM must be transferred the Stellar account.
    :param CliSession cli_session: Current CLI session.
    :param str account_address: Address of the new account.
    :param str amount: XLM amount to transfer to the new account.
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """
    seed = _fetch_valid_seed(cli_session)
    if seed is None:
        return

    if not is_valid_address(account_address):
        print('The given account address is invalid')
        return

    if yes_or_no_input('To create the new account, a payment of {} XLM will be done '
                       'to the following address {}. Are you sure you want to proceed?'
                       .format(amount, account_address)) == USER_INPUT_NO:
        return

    builder = Builder(secret=seed)
    builder.add_text_memo(transaction_memo)
    builder.append_create_account_op(
        destination=account_address,
        starting_balance=amount,
        source=cli_session.account_address)
    response = _sign_and_submit_operation(builder)
    #process_server_payment_response(response) # TODO: Parse response


def fund_using_friendbot(account_address):
    """
    This method is used to request the Stellar Friendbot to fund the given account
    address. This will only work on the Stellar testnet.
    :param str account_address: Account address to be funded.
    :return: Returns a string with the result of the fund request.
    :rtype: str
    """
    if not is_valid_address(account_address):
        return 'The given account address is invalid.'

    try:
        r = requests.get('{}/friendbot?addr={}'.format(STELLAR_HORIZON_TESTNET_URL, account_address))
        return 'Successful transaction request' if is_successful_http_status_code(r.status_code) \
            else 'Failed transaction request (Maybe this account was already funded by Friendbot). Status code {}'.\
            format(r.status_code)
    except requests.exceptions.ConnectionError:
        return "A connection error occurred (Please check your Internet connection)"


def send_payment(cli_session, destination_address, token_code, amount, token_issuer=None, transaction_memo=''):
    """
    This method is used to send a transaction of the specified token to a given address.
    :param CliSession cli_session: Current CLI session.
    :param str destination_address: Destination address.
    :param str amount: Amount to be sent.
    :param str token_code: Code of the token to be sent.
    :param str token_issuer: Issuer of the token to be sent. It can be None when dealing with native asset (XLM).
    :param str transaction_memo: Text memo to be included in Stellar transaction. Maximum size of 28 bytes.
    """

    seed = _fetch_valid_seed(cli_session)
    if seed is None:
        return

    if not is_valid_address(destination_address):
        print('The given destination address is invalid')
        return
    if destination_address == cli_session.account_address:
        print('Sending payment to own address. This is not allowed')
        return
    if token_issuer is not None and not is_valid_address(token_issuer):
        print('The given token issuer address is invalid')
        return
    if not is_valid_transaction_text_memo(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    if yes_or_no_input('A payment of {} {} will be done to the following address {}. Are you sure you want to proceed?'
                       .format(amount, token_code, destination_address)) == USER_INPUT_NO:
        return

    builder = Builder(secret=seed)
    builder.add_text_memo(transaction_memo)
    builder.append_payment_op(
        destination=destination_address,
        amount=amount,
        asset_issuer=token_issuer,
        asset_code=token_code)
    response = _sign_and_submit_operation(builder)
    process_server_payment_response(response)


def send_path_payment(cli_session, destination_address,
                      code_token_to_send, max_amount_to_send, issuer_token_to_send,
                      code_token_to_be_received, amount_to_be_received, issuer_token_to_be_received,
                      transaction_memo=''):
    seed = _fetch_valid_seed(cli_session)
    if seed is None:
        return

    if not is_valid_address(destination_address):
        print('The given destination address is invalid')
        return

    # TODO: Incomplete


def establish_trustline(cli_session, destination_address, token_code, token_limit, transaction_memo=''):
    seed = _fetch_valid_seed(cli_session)
    if seed is None:
        return

    if not is_valid_address(destination_address):
        print('The given destination address is invalid')
        return
    if destination_address == cli_session.account_address:
        print('Sending change of trust transaction to own address. This is not allowed')
        return
    if not is_valid_transaction_text_memo(transaction_memo):
        print('The maximum size of the text memo is {} bytes'.format(STELLAR_MEMO_TEXT_MAX_BYTES))
        return

    builder = Builder(secret=seed)
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
    except Exception:
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


def _fetch_valid_seed(cli_session):
    seed = cli_session.account_seed
    if seed is None \
            or not is_valid_seed(seed) \
            or not is_address_matching_seed(seed, cli_session.account_address):
        seed = _ask_for_user_seed(cli_session,
                                  "Either no seed was found for this CLI session account, "
                                  "the seed for this CLI session account is invalid or "
                                  "the seed does match the current CLI session account address. "
                                  "No transaction can be made without a valid seed. Please "
                                  "insert your seed to process the transaction")
    return seed


def _ask_for_user_seed(cli_session, msg):
    seed = password_input(msg)
    if not is_valid_seed(seed):
        print('The given seed is invalid')
        return None

    if not is_address_matching_seed(seed, cli_session.account_address):
        print('The given seed does not match with the address of the current CLI session')
        return None

    if yes_or_no_input('Do you want to save the seed for this CLI session account?') == USER_INPUT_YES:
        cli_session.account_seed = seed

    return seed
