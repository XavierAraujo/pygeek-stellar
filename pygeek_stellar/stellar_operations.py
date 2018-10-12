
# 3rd party imports
from stellar_base.operation import *


def create_account_creation_op(destination, starting_balance, source=None):
        """
        This method creates a Stellar account creation operation. This operation can be used
        to create a new Stellar account by transferring a certain amount of funds to it.
        :param str destination: Address of the new account to be created.
        :param str starting_balance: Amount of funds to transfer to the new account.
        :param str source:
        :return: Returns the newly created operation.
        :rtype: CreateAccount
        """
        return CreateAccount(opts={
            'source': source,
            'destination': destination,
            'starting_balance': starting_balance
        })


def create_payment_op(destination, amount, asset_code='XLM', asset_issuer=None, source=None):
    """
    This method creates a Stellar payment operation. This operation can be used
    to transfer funds between two accounts.
    :param str destination: Destination address to which the funds must be sent.
    :param str amount: Amount of funds to transfer.
    :param str asset_code: Code of the asset to be transferred. If none is specified the native asset is chosen.
    :param str asset_issuer: Issuer of the asset.
    :param str source:
    :return: Returns the newly created operation.
    :rtype: Payment
    """
    return Payment(opts={
        'source': source,
        'destination': destination,
        'asset': Asset(asset_code, asset_issuer),
        'amount': amount
    })


def create_trust_op(destination, code, limit=None, source=None):
    """
    This method creates a Stellar trust operation. This operation can be used
    to create, delete or update an existing trustline.
    :param str destination: Destination address to which the trustline refers.
    :param str code: Code of the asset to which the trustline refers.
    :param str limit: Amount limit of the asset for the trustline.
    :param str source:
    :return: Returns the newly created operation.
    :rtype: ChangeTrust
    """
    return ChangeTrust(opts={
        'source': source,
        'asset': Asset(code, destination),
        'limit': limit
    })

