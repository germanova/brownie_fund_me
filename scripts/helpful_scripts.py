from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

# only 8 decimals because in getPrice() function we already multiply by 10 zeroes
DECIMALS = 8
STARTING_PRICE = 200000000000

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.load(config["wallets"]["account_name"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print(f"Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        # Web3.toWei() just add 18 decimals to de value: Web3.toWei(STARTING_PRICE, "ether")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
