from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENV


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pf_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        pf_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        pf_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    return fund_me


def main():
    deploy_fund_me()
