# Firefly Stocks Accounter

A Python program to track investment balances in [Firefly](https://www.firefly-iii.org/), by pooling end-of-day data of your positions and updating a predefined asset account. This allows you to have a complete picture of your finances in Firefly - including your investments.

This isn't meant to replace your favourite brokers's investment app/website or track real time data. It's just a way to have a somewhat up-to-date representation of your investment balance available in Firefly.

## Requirements
* python >= 3.11

## Setup

> **Note:** The program currently relies on the end-of-day market data API from https://eodhd.com/. You will have to create a free account which - at the time of writing - offers 20 daily API calls plus 500 lifetime extra calls in the free tier. Each query to a different market ticker is 1 call. Assuming you have less than 20 positions and run this once per day, you should never hit the limit of the free tier. Given that the aim of this program isn't to provide live asset tracking I found this to be a good enough compromise for my use case.
>
> On every program run it'll print the number of available API tokens so you can keep track of your current usage.

### Steps

* Create an account at https://eodhd.com/ and retrieve your API token.
* Copy `settings.example.toml` into `settings.toml` and adjust the settings - the parameters are explained in the settings file itself.
* Install the python dependencies:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

* Run the script with `python accounter.py` or set up a cronjob to run it periodically.
