from datetime import datetime
from decimal import Decimal

import requests


class EODHDProvider:
    BASE_URL = "https://eodhd.com/api"

    def __init__(self, config):
        self.token = config["api"]["token"]

    def get_user_data(self):
        response = requests.get(
            f"{self.BASE_URL}/user", params={"api_token": self.token}
        )
        response.raise_for_status()
        return response.json()

    def get_api_calls_info(self) -> tuple[int, int, int]:
        user_data = self.get_user_data()
        return (
            user_data["apiRequests"],
            user_data["dailyRateLimit"],
            user_data["extraLimit"],
        )

    def get_ticker_historical_data(self, ticker: str):
        response = requests.get(
            f"{self.BASE_URL}/eod/{ticker}",
            params={"api_token": self.token, "fmt": "json"},
        )
        response.raise_for_status()
        return response.json()

    def get_latest_eod_ticker_value(self, ticker: str) -> Decimal:
        data = self.get_ticker_historical_data(ticker)
        latest_data = max(data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        return Decimal(str(latest_data.get("close")))


class FireflyProvider:
    BASE_URL = ""

    def __init__(self, config):
        self.BASE_URL = f"{config['firefly']['address']}/api/v1"
        self.token = config["firefly"]["token"]
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
            "Accept": "application/json",
        }

    def get_system_information(self):
        response = requests.get(f"{self.BASE_URL}/about", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_asset_accounts(self):
        response = requests.get(
            f"{self.BASE_URL}/accounts/", headers=self.headers, params={"type": "asset"}
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def find_account(self, account_name: str):
        accounts = self.get_asset_accounts()
        for account in accounts:
            if account["attributes"]["name"] == account_name:
                return account
        return None

    def get_account(self, account_id: int):
        response = requests.get(
            f"{self.BASE_URL}/accounts/{account_id}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_asset_account(self, account_name: str, balance: Decimal):
        response = requests.post(
            f"{self.BASE_URL}/accounts",
            headers=self.headers,
            json={
                "name": account_name,
                "opening_balance": str(balance),
                "opening_balance_date": datetime.now().isoformat(),
                "type": "asset",
                "account_role": "defaultAsset",
            },
        )
        response.raise_for_status()
        return response

    def create_transaction(
        self,
        account_id: int,
        amount: Decimal,
        description: str,
        withdrawal: bool = False,
    ):
        response = requests.post(
            f"{self.BASE_URL}/transactions",
            headers=self.headers,
            json={
                "transactions": [
                    {
                        "type": "withdrawal" if withdrawal else "deposit",
                        "date": datetime.now().isoformat(),
                        "amount": str(amount),
                        "description": description,
                        "source_id": str(account_id) if withdrawal else None,
                        "destination_id": str(account_id) if not withdrawal else None,
                    }
                ]
            },
        )
        response.raise_for_status()
        return response
