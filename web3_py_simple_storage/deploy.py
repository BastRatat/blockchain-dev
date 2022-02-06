import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv


load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

simple_storage = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]

bytecode = simple_storage["evm"]["bytecode"]["object"]
abi = simple_storage["abi"]

# Ropsten
ropsten_url = os.getenv("ROPSTEN_URL")
ropsten_chain_id = 3
personal_address = "0x964c8D8A82a028275a5c87Ad6E38B3ED7EAfA063"
private_key = os.getenv("PRIVATE_KEY")

# Ganache
ganache_url = "HTTP://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(ropsten_url))
chain_id = 1337
ganache_private_key = os.getenv("GANACHE_PRIVATE_KEY")
address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(personal_address)

# DEPLOY
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": ropsten_chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": personal_address,
        "nonce": nonce,
    }
)
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
simple_storage_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print("deployed")

# INTERACT
store_transaction = simple_storage_contract.functions.store(15).buildTransaction(
    {
        "chainId": ropsten_chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": personal_address,
        "nonce": nonce + 1,
    }
)
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
tx_store_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_store_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)
print(simple_storage_contract.functions.retrieve().call())
# simple_storage_contract.functions.retrieve().call() should output 15
