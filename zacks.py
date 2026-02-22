import pandas as pd
import requests
import time
import argparse


def clean_ticker(ticker: str) -> str:
    """
    Remove suffixes such as -CT from tickers.
    Example: NVDA-CT -> NVDA
    """
    ticker = str(ticker).strip().upper()

    if "-" in ticker:
        ticker = ticker.split("-")[0]

    return ticker


def get_zacks_rank(ticker):
    url = f"https://quote-feed.zacks.com/index?t={ticker}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if ticker in data:
            rank = data[ticker].get("zacks_rank")
            rank_text = data[ticker].get("zacks_rank_text")
            name = data[ticker].get("name")

            return rank, rank_text, name

    except Exception:
        pass

    return None, None, None


def main():
    parser = argparse.ArgumentParser(description="Fetch Zacks ranks for stocks")

    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--column", default="stock")
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    if args.column not in df.columns:
        raise ValueError(f"Column '{args.column}' not found in CSV")

    rows = []

    for raw_ticker in df[args.column]:
        cleaned = clean_ticker(raw_ticker)

        rank, rank_text, name = get_zacks_rank(cleaned)

        if args.verbose:
            print(f"{raw_ticker} -> {cleaned} -> {rank}")

        rows.append({
            "original_ticker": raw_ticker,
            "ticker": cleaned,
            "name": name,
            "rank": rank,
            "rank_text": rank_text
        })

        time.sleep(args.delay)

    result = pd.DataFrame(rows)

    # Convert rank to numeric for sorting
    result["rank_numeric"] = pd.to_numeric(result["rank"], errors="coerce")

    # Stocks without rank go to bottom
    result = result.sort_values(by="rank_numeric", na_position="last")

    result.drop(columns=["rank_numeric"], inplace=True)

    result.to_csv(args.output_csv, index=False)

    print(f"\nSaved results to {args.output_csv}")


if __name__ == "__main__":
    main()
