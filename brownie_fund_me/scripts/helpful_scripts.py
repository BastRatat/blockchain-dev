from brownie import network, config, accounts, MockV3Aggregator

DECIMALS = 8
INITIAL_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork-dev", "mainnet-fork"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"Active network is {network.show_active}.")
    print("Deploying mocks")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, INITIAL_PRICE, {"from": get_account()})
        print("Mocks deployed")
