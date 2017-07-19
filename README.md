# CryptoMonitor

## Objective

The application is to monitor the cryptocurrency prices, spot the arbitrage
opportunity, and notify the users in Slack.

The market data source is from [CoinMarketCap](https://coinmarketcap.com).

## Compatibility

Python 3.x

## Installation

Currently it is still in beta version so the package is not released in PyPi.

```
pip install git+https://github.com/Aurora-Team/CryptoMonitor.git
```

## Preparation

First create a Slack app and create a API key from their official [website](https://api.slack.com/).

Second, run the command with the API key and a list of instruments.

For example, to run the symbol Ripple and Tether at a price discrepancy of 7%, run
the command

```
cryptomon -key <api_key> -pair ripple 0.07 -pair tether 0.07
```

## Functional enhancement

The application is still under experiments. Please raise your proposed
functional enhancement in the Issue tab. We are happy with your input and
will review and implement it soon.

