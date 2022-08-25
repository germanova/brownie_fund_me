from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()

    # publish_source = True es para verificar con el API personal de etherscan que está en .env

    # pass the price feed address to our fundme contract, before the from,
    # Address can be found in the eth price feed documentation of Chainlink,
    # here we use ETH /USD address of Rinkeby Testnet

    # if we are on a persistent network like rinkeby use the associated priceFeed address
    # otherwise, deploy mocks for ganache. Mocks are stored at contracts/test folder

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        deploy_mocks()
        # use the most recently deployed mock
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks Deployed!")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fund_me.address}")
    # the return is so that the test_fund_me.py works
    return fund_me


def main():
    deploy_fund_me()
