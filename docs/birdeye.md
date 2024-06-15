# Premium APIs

## Supported Networks
``get`` https://public-api.birdeye.so/defi/networks

Get a list of all supported networks.
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/networks"

headers = {"X-API-KEY": "your_api_key_here"}

response = requests.get(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": [
    "solana",
    "ethereum",
    "arbitrum",
    "avalanche",
    "bsc",
    "optimism",
    "polygon",
    "base",
    "zksync",
    "sui"
  ],
  "success": true
}
```
## Request History
``get`` https://public-api.birdeye.so/defi/history

Get list of all historical API calls from the authorized user, and check the remaining time (in seconds) until expiration. Make sure to RENEW the package BEFORE expiration time to avoid service interruption. This API endpoint will be decommissioned on June 10th, 2024
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/history"

headers = {"X-API-KEY": "your_api_key_here"}

response = requests.get(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": {
    "items": [],
    "resetInSeconds": 0
  },
  "success": true
}
```
## Price
``get`` https://public-api.birdeye.so/defi/price

Get price update of a token.
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/price?address=So11111111111111111111111111111111111111112"

headers = {"X-API-KEY": "your_api_key_here"}

response = requests.get(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": {
    "value": 143.94093686354378,
    "updateUnixTime": 1718434958,
    "updateHumanTime": "2024-06-15T07:02:38"
  },
  "success": true
}
```
## Price - Multiple (GET Method)
``get`` https://public-api.birdeye.so/defi/multi_price

Get price updates of multiple tokens in a single API call. Maximum 100 tokens
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/multi_price?list_address=So11111111111111111111111111111111111111112%2CmSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"

headers = {"X-API-KEY": "your_api_key_here"}

response = requests.get(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": {
    "So11111111111111111111111111111111111111112": {
      "value": 144.47853340269344,
      "updateUnixTime": 1718435265,
      "updateHumanTime": "2024-06-15T07:07:45",
      "priceChange24h": -2.239618712529462
    },
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {
      "value": 172.53767748962224,
      "updateUnixTime": 1718435197,
      "updateHumanTime": "2024-06-15T07:06:37",
      "priceChange24h": -2.5207426869715355
    }
  },
  "success": true
}
```
## Price - Multiple (POST method)
``post`` https://public-api.birdeye.so/defi/multi_price

Get price updates of multiple tokens in a single API call. Maximum 100 tokens
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/multi_price"

headers = {
    "content-type": "application/json",
    "X-API-KEY": "your_api_key_here"
}

response = requests.post(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": {
    "So11111111111111111111111111111111111111112": {
      "value": 144.47853340269344,
      "updateUnixTime": 1718435265,
      "updateHumanTime": "2024-06-15T07:07:45",
      "priceChange24h": -2.239618712529462
    },
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {
      "value": 172.53767748962224,
      "updateUnixTime": 1718435197,
      "updateHumanTime": "2024-06-15T07:06:37",
      "priceChange24h": -2.5207426869715355
    }
  },
  "success": true
}
```
## Price - Historical
``get`` https://public-api.birdeye.so/defi/history_price

Get historical price line chart of a token.
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/history_price?address=So11111111111111111111111111111111111111112&address_type=token&type=15m&time_from=1718374417&time_to=1718460817"

headers = {
    "x-chain": "solana",
    "X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"
}

response = requests.get(url, headers=headers)

print(response.text)
```
### Example Response
```json
{
  "data": {
    "items": [
      {
        "unixTime": 1718374500,
        "value": 145.64484229125435
      },
      {
        "unixTime": 1718375400,
        "value": 144.3111424021901
      },
	  // ... [output truncated]
      {
        "unixTime": 1718459100,
        "value": 144.26438994469314
      },
      {
        "unixTime": 1718460000,
        "value": 144.26438994469314
      }
    ]
  },
  "success": true
}
```
## Trades - Token
``get`` https://public-api.birdeye.so/defi/txs/token

Get list of trades of a certain token.
### Code
```python
import requests

url = "https://public-api.birdeye.so/defi/txs/token?address=So11111111111111111111111111111111111111112&offset=0&limit=10&tx_type=all"

headers = {
    "x-chain": "solana",
    "X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"
}

response = requests.get(url, headers=headers)

print(response.text)
```
## Trades - Pair
``get`` https://public-api.birdeye.so/defi/txs/pair

Get list of trades of a certain pair or market.

```python
import requests

url = "https://public-api.birdeye.so/defi/txs/pair?address=9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT&tx_type=swap&sort_type=desc"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## OHLCV
``get`` https://public-api.birdeye.so/defi/ohlcv

Get OHLCV price of a token.

```python
import requests

url = "https://public-api.birdeye.so/defi/ohlcv?address=So11111111111111111111111111111111111111112&type=15m"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## OHLCV - Pair
``get`` https://public-api.birdeye.so/defi/ohlcv/pair

Get OHLCV price of a pair.
```python
import requests

url = "https://public-api.birdeye.so/defi/ohlcv/pair?address=9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT&type=15m"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## OHLCV - Base/Quote
``get`` https://public-api.birdeye.so/defi/ohlcv/base_quote

Get OHLCV price of a base-quote pair.

```python
import requests

url = "https://public-api.birdeye.so/defi/ohlcv/base_quote?base_address=So11111111111111111111111111111111111111112&quote_address=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&type=15m"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## Token - List
``get`` https://public-api.birdeye.so/defi/tokenlist

Get token list of any supported chains.

```python
import requests

url = "https://public-api.birdeye.so/defi/tokenlist?sort_by=v24hUSD&sort_type=desc"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## Token - Security
``get`` https://public-api.birdeye.so/defi/token_security

Get token security of any supported chains.
```python
import requests

url = "https://public-api.birdeye.so/defi/token_security?address=So11111111111111111111111111111111111111112"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
# Token - Overview
``get`` https://public-api.birdeye.so/defi/token_overview

Get overview of a token.
```python
import requests

url = "https://public-api.birdeye.so/defi/token_overview?address=So11111111111111111111111111111111111111112"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```
## Token - Creation Token Info
``get`` https://public-api.birdeye.so/defi/token_creation_info

Get creation info of token
```python
import requests

url = "https://public-api.birdeye.so/defi/token_creation_info?address=D7rcV8SPxbv94s3kJETkrfMrWqHFs6qrmtbiu6saaany"

headers = {"X-API-KEY": "dc786d8cf5524126941fc415c048b0b9"}

response = requests.get(url, headers=headers)

print(response.text)
```