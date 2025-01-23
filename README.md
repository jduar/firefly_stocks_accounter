# Firefly Stocks Accounter

A Python program to track investment balances in [Firefly](https://www.firefly-iii.org/), by pooling end-of-day data of your positions and updating a predefined asset account. This allows you to have a complete picture of your finances in Firefly - including your investments.

This isn't meant to replace your favourite brokers's investment app/website or track real time data. It's just a way to have a somewhat up-to-date representation of your investment balance available in Firefly.

## Setup

> **Note:** The program currently relies on the end-of-day market data API from https://eodhd.com/. You will have to create a free account which - at the time of writing - comes with 520 free API tokens. Each call for value information on each different ticker costs 1 token. Assuming you're tracking 5 different positions and run this script weekly, those should be good for around 2 years of free usage. Given that the aim of this program isn't to provide live asset tracking I found this to be a good enough compromise for my use case.
>
> On every program run it'll print the number of available API tokens so you can keep track of your current usage. You have been warned.

* Create an account at https://eodhd.com/ and retrieve your API token.
* Copy `settings.example.toml` into `settings.toml` and adjust the settings - the parameters are explained in the settings file itself.
* Run the script with `python accounter.py` or set up a cronjob to run it periodically.
