# Zacks Rank 1 Stock Extractor

This tool reads a CSV file containing stock tickers and extracts the ones that have a **Zacks Rank of 1 (Strong Buy)** using the public Zacks quote feed.

The filtered stocks are saved into a new CSV file.

---

## Requirements

* Python 3.8 or newer
* Internet connection

Install dependencies:

```
pip install pandas requests
```

---

## Input CSV format

Your CSV must contain a column with stock tickers.

Example:

```
stock
AAPL
MSFT
NVDA
TSLA
```

---

## Basic Usage

```
python zacks.py --input_csv stocks.csv --output_csv rank1_stocks.csv

---

## Arguments

Required arguments:

```
--input_csv
```
Path to the CSV containing stock tickers.

```
--output_csv
```
Path where the filtered CSV will be saved.

Optional arguments:
```
--column
```
Column name containing tickers.
Default: stock
```
--delay
```
Delay between API requests in seconds.
Default: 0.4
```
--verbose
```
Print progress while running.

---

## Example with optional arguments

```
python zacks.py 
--input_csv stocks.csv 
--output_csv rank1.csv 
--column ticker 
--delay 0.2 
--verbose
```
---

## Output

The output CSV contains only stocks with Zacks Rank = 1.

Example output:
```
ticker,name,rank
NVDA,NVIDIA Corporation,Strong Buy
```
---

## Notes

* The script includes a delay between requests to reduce the risk of being rate limited.
* Invalid or unknown tickers are skipped automatically.

