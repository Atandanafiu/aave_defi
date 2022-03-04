
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
    borrowed_eth, total_eth get_borrowable_data(lending_pool, account)


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
