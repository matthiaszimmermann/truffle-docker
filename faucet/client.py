import json
import sys

from argparse import ArgumentParser, Namespace
from decimal import Decimal
from web3 import Web3
from web3.contract import Contract

WEB3_URI = 'http://host.docker.internal:7545'
TRUFFLE_JSON = '/app/faucet/build/contracts/Faucet.json'


def main():
    cli_args = get_args()
    web3 = get_web3(WEB3_URI)
    
    amount = cli_args.amount
    method = 'withdraw'
    method_args = [ get_amount_wei(web3, amount, 'ether') ]
    gas = 2000000

    print('balance before {} eth account {}'.format(get_balance(web3, cli_args.address, 'ether'), cli_args.address))

    txn_hash = contract_call(
        cli_args.address, cli_args.pkey, # sender data
        web3, TRUFFLE_JSON,              # web3 provider and contract data
        method, method_args, gas)        # method call data

    print('balance  after {} eth account {}'.format(get_balance(web3, cli_args.address, 'ether'), cli_args.address))


def get_args() -> Namespace():
    parser = ArgumentParser(description='faucet contract method call demo')
    parser.add_argument('-a', '--address', required=True, help='account address', )
    parser.add_argument('-k', '--pkey', required=True, help='account private key')
    parser.add_argument('amount', help='requested amount [eth]')
    args = parser.parse_args()

    print('address {}'.format(args.address))
    print('pkey {}'.format(args.pkey))
    print('amount {}'.format(args.amount))

    return args


def contract_call(address: str, pkey: str, web3: Web3, truffle_json: str, method: str, args: list, gas: int) -> str:
    contract = get_contract(web3, truffle_json)

    chain_id = web3.eth.chain_id
    gas_price =  web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(address)

    txn = get_txn(
        contract, method, args, gas, 
        chain_id, gas_price, nonce)
    
    txn_hash = sign_and_send(web3, pkey, txn)


def get_web3(web3_uri: str) -> Web3:
    web3 = Web3(Web3.HTTPProvider(web3_uri))
    chain_id = web3.eth.chain_id
    connected = web3.isConnected()
    print('web3 provider {} chain id {} connected {}'.format(web3_uri, chain_id, connected))

    return web3


def get_contract(web3: Web3, truffle_json: str) -> Contract:
    truffle = json.load(open(truffle_json))
    chain_id = str(web3.eth.chain_id)
    address = truffle['networks'][chain_id]['address']
    abi = truffle['abi']
    name = truffle['contractName']
    contract = web3.eth.contract(address=address, abi=abi)

    print('contract object created: {}'.format(name))
    print('contract address: {}'.format(address))

    return contract


def get_txn(contract: Contract, method: str, args: list, gas: int, chain_id: int, gas_price: int, nonce: str) -> map:
    txn = contract.functions[method](*args).buildTransaction({
        'chainId': chain_id,
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce
    })

    print('txn created {}'.format(txn))

    return txn


def sign_and_send(web3: Web3, pkey: str, txn: map) -> str:
    signed = web3.eth.account.sign_transaction(txn, pkey)
    txn_hash = web3.eth.send_raw_transaction(signed.rawTransaction)

    print('txn successfully sent. txn hash {}'.format(txn_hash))

    return txn_hash


def get_amount_wei(web3: Web3, amount: str, unit: str) -> int:
    amount_wei = web3.toWei(Decimal(amount), unit)
    print('amount in wei {}'.format(amount_wei))

    return int(amount_wei)


def get_balance(web3: Web3, address: str, unit='wei') -> Decimal:
    amount_wei = web3.eth.get_balance(address)
    return web3.fromWei(amount_wei, unit)


if __name__ == "__main__":
    main()
