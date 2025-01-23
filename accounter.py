import tomllib
from providers import EODHDProvider, FireflyProvider

from decimal import Decimal

with open("settings.toml", "rb") as f:
    config = tomllib.load(f)

eodhd_provider = EODHDProvider(config)
firefly_provider = FireflyProvider(config)


def main():
    print("**********")

    stocks_balance = get_stock_accounts_balance()
    update_firefly_stocks_account(config["firefly"]["account"], stocks_balance)

    used_tokens, daily_limit, extraLimits = eodhd_provider.get_api_calls_info()
    print(f"\nAvailable API tokens: {daily_limit-used_tokens+extraLimits}")


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
