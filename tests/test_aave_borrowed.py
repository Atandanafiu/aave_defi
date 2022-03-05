from scripts.aave_borrow import (
    approve_erc20, get_account, get_asset_price, get_lending_pool, get_weth)
from brownie import network, config


def test_get_asset_price():
    # Arrange/ Act
    asset_price = get_asset_price()
    # Assert
    assert asset_price > 0


def test_get_lending_pool():
    # Arrange /Act
    lending_pool = get_lending_pool()
    # Assert
    assert lending_pool is not None


def test_approve_erc20():
    # Arrange
    account = get_account()
    lending_pool = get_lending_pool()
    amount = 1000000000000000000  # 1
    erc20_address = config["neworks"][network.show_active()]["weth_token"]
    # ACT
    approved = approve_erc20(
        amount, lending_pool.address, erc20_address, account)
    # Assert
    assert approved is True
