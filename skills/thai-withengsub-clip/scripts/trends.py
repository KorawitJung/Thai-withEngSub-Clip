"""Fetch Google Trends series and test how two terms move together.

usage:
  uv run --with pytrends --with "urllib3<2" --with pandas --with scipy $SKILL/scripts/trends.py fetch data.json "ดูดวง" "หางาน" --geo TH --from 2019-01-01 --to 2026-10-31
  uv run --with pandas --with scipy $SKILL/scripts/trends.py corr data.json "ดูดวง" "หางาน"

A fetch takes at most 5 terms, because Trends scales terms against each other. Compare only terms from the same fetch.
Report the year-over-year and monthly-change results. The level result is printed only as a warning:
two series that both drift over time correlate highly without moving together.
"""
import argparse
import json
from pathlib import Path


def fetch(args):
    if not 1 <= len(args.terms) <= 5:
        raise SystemExit("fetch takes 1 to 5 terms")
    from pytrends.request import TrendReq

    client = TrendReq(hl="th-TH", tz=420, retries=3, backoff_factor=8)
    client.build_payload(args.terms, geo=args.geo, timeframe=f"{args.start} {args.end}")
    frame = client.interest_over_time()
    if frame.empty:
        raise SystemExit("Trends returned no data")
    frame = frame.drop(columns=["isPartial"], errors="ignore")
    frame.index = frame.index.strftime("%Y-%m")
    Path(args.out).write_text(json.dumps(frame.to_dict(), ensure_ascii=False), encoding="utf-8")
    print(f"wrote {args.out}: {len(frame)} points, {frame.index[0]} to {frame.index[-1]}")


def corr(args):
    import pandas as pd
    from scipy import stats

    data = pd.DataFrame(json.loads(Path(args.data).read_text(encoding="utf-8"))).sort_index().astype(float)
    pair = data[[args.a, args.b]].dropna()
    for name, part in (("level (drift warning)", pair), ("year-over-year", pair.diff(12).dropna()), ("monthly change", pair.diff().dropna())):
        result = stats.spearmanr(part[args.a], part[args.b])
        print(f"{name}: r={result.statistic:.2f} p={result.pvalue:.3g} n={len(part)}")
    months = data[args.a].groupby(data.index.str[5:]).mean()
    top = months.idxmax()
    print(f"{args.a} peak month {top}: {months[top] / months.drop(top).mean() - 1:+.0%} against the other months")
    years = data[args.a].groupby(data.index.str[:4]).mean()
    print(f"{args.a} first to last year: {years.iloc[0]:.1f} to {years.iloc[-1]:.1f}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    one = sub.add_parser("fetch")
    one.add_argument("out")
    one.add_argument("terms", nargs="+")
    one.add_argument("--geo", default="TH")
    one.add_argument("--from", dest="start", default="2019-01-01")
    one.add_argument("--to", dest="end", required=True)
    one.set_defaults(run=fetch)
    two = sub.add_parser("corr")
    two.add_argument("data")
    two.add_argument("a")
    two.add_argument("b")
    two.set_defaults(run=corr)
    args = ap.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
