from brownie import accounts, config, SimpleStorage, network


def deploy_contract():
    # account = accounts.load("learn-brownie-account")
    # account = accounts.add(config["wallets"]["from_key"])
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    stored_value = simple_storage.retrieve()
    print(stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_contract()
