from decimal import Decimal

import tomllib
from requests.exceptions import ConnectionError, HTTPError

from providers import EODHDProvider, FireflyProvider

with open("settings.toml", "rb") as f:
    config = tomllib.load(f)

eodhd_provider = EODHDProvider(config)
firefly_provider = FireflyProvider(config)


def main():
    print("********** Firefly Stocks Accounter\n")

    # Ensure the connection to Firefly is working before advancing to avoid wasting EODHD API calls
    check_firefly_connection()

    stocks_balance = get_stock_accounts_balance()
    update_firefly_stocks_account(config["firefly"]["account"], stocks_balance)

    used_tokens, daily_limit, extraLimits = eodhd_provider.get_api_calls_info()
    print(f"\nAvailable API tokens: {daily_limit-used_tokens+extraLimits}")


def check_firefly_connection():
    try:
        firefly_provider.get_system_information()
    except HTTPError as http_err:
        if http_err.response.status_code == 401:
            print(
                "** Unauthorized connection to Firefly server. Check your configured personal access token."
            )
        else:
            print(http_err)
        exit()
    except ConnectionError as connection_err:
        print(
            f"** Unable to connect to the Firefly server. Check your settings.\n\nError detail: {connection_err}"
        )
        exit()


def get_stock_accounts_balance() -> Decimal:
    balance = Decimal(0)
    positions = config["stocks"]["positions"]

    for ticker, amount in positions:
        balance += eodhd_provider.get_latest_eod_ticker_value(ticker) * amount
    return balance


def update_firefly_stocks_account(account_name: str, account_balance: Decimal):

    account = firefly_provider.find_account(account_name)
    if account is None:
        firefly_provider.create_asset_account(account_name, account_balance)
        action = "created"
    else:
        old_balance = Decimal(account["attributes"]["current_balance"])
        if old_balance > account_balance:
            withdrawal = True
        elif old_balance < account_balance:
            withdrawal = False
        else:
            print(
                f"Account {account_name} balance hasn't changed. Current balance: {account_balance}."
            )
            return

        firefly_provider.create_transaction(
            account["id"],
            abs(old_balance - account_balance),
            description="Automatic account update",
            withdrawal=withdrawal,
        )
        action = "updated"
    print(f"Account {account_name} {action}. Current balance: {account_balance}.")


if __name__ == "__main__":
    main()
