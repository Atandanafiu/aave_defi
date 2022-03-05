
from brownie import network, config, interface, web3
from scripts.hepful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3


# Globel variable
amount = web3.toWei(0.01, "Ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["kovan"]:
        get_weth()
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print(" Depositing...")
    tx = lending_pool.deposit(erc20_address, amount,
                              account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited")
    borrowed_eth, total_eth = get_borrowable_data(lending_pool, account)
    print("Let_borrow_dai")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"])
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowed_eth * 0.95)
    # borrowable_eth  --> borrowable_dai * 0.95
    print(f"We are borrowing {amount_dai_to_borrow} DAI")

    # We'll borrow
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address, web3.toWei(amount_dai_to_borrow, "ether"), 1, 0, account.address, {"from": account})
    borrow_tx.wait(1)
    print("We borrow some DAI")
    get_borrowable_data(lending_pool, account)
    repay_all(amount, lending_pool, account)
    print("You just deposited, borrowed, and repay with Aave, brownie, and chainlink too")


def repay_all(amount, lending_pool, account):
    approve_erc20(web3.toWei(amount, lending_pool,
                  config["networks"][network.show_active()]["dai_token"], account))
    repay_tx = lending_pool.repay(config["networks"][network.show_active(
    )]["dai_token"], amount, 1, account.address, {"from": account})
    repay_tx.wait(1)
    print("Repayed!!!!!!!!!!!")


def get_asset_price(pricefeedAdress):
    dai_eth_price_feed = interface.AggregatorV3interface(pricefeedAdress)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    coverted_latest_price = web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH prce is {coverted_latest_price}")
    return float(coverted_latest_price)


def get_borrowable_data(lending_pool, account):
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_eth,
     ltv, health_factor) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = web3.fromWeiz(total_debt_eth, "ether")
    print(f"You can borrow{available_borrow_eth} worth of ETH deployed")
    print(f"You have{total_collateral_eth} worth of ETH deployed")
    print(f"You have {total_debt_eth} worth of ETH deployed")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 Token !!!!!!! ")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(2)
    print("Approved!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return tx


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active(
    )]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    # ABI
    # Address -- check!
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
