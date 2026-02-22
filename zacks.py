import pandas as pd
import requests
import time
import argparse


def get_zacks_rank(ticker):
    url = f"https://quote-feed.zacks.com/index?t={ticker}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if ticker in data:
            rank = data[ticker]["zacks_rank"]
            rank_text = data[ticker]["zacks_rank_text"]
            name = data[ticker]["name"]

            return rank, rank_text, name
    except Exception:
        pass

    return None, None, None


def main():
    parser = argparse.ArgumentParser(
        description="Extract stocks with Zacks Rank 1 from a CSV file"
    )

    parser.add_argument(
        "--input_csv",
        required=True,
        help="Path to input CSV file"
    )

    parser.add_argument(
        "--output_csv",
        required=True,
        help="Path to output CSV file"
    )

    parser.add_argument(
        "--column",
        default="stock",
        help="Column name containing stock tickers (default: stock)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.4,
        help="Delay between API calls in seconds (default: 0.4)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress information"
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    if args.column not in df.columns:
        raise ValueError(f"Column '{args.column}' not found in CSV")

    rank1 = []

    for ticker in df[args.column]:
        ticker = str(ticker).strip()

        rank, rank_text, name = get_zacks_rank(ticker)

        if args.verbose:
            print(f"{ticker} -> {rank}")

        if rank == 1:
            rank1.append({
                "ticker": ticker,
                "name": name,
                "rank": rank_text
            })

        time.sleep(args.delay)

    result = pd.DataFrame(rank1)
    result.to_csv(args.output_csv, index=False)

    print(f"\nSaved {len(result)} Rank-1 stocks to {args.output_csv}")


if __name__ == "__main__":
    main()
