"""Compare two windows of normalized Search Console query-by-page rows."""

import argparse
import csv
import math
import sys
from datetime import date
from pathlib import Path


KEY_FIELDS = ("country", "device", "search_type", "query", "page")
WINDOWS = ("prior", "current")
METRICS = ("clicks", "impressions", "position")
REQUIRED = {*KEY_FIELDS, *METRICS, "window", "start_date", "end_date"}


def read_pairs(path, query):
    dates = {}
    pairs = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not REQUIRED.issubset(reader.fieldnames or []):
            missing = ", ".join(sorted(REQUIRED.difference(reader.fieldnames or [])))
            raise ValueError(f"Missing normalized CSV columns: {missing}")
        for row in reader:
            if None in row or any(row[field] is None for field in REQUIRED):
                raise ValueError(f"Line {reader.line_num}: column count does not match the header")
            key = tuple(row[field].strip() for field in KEY_FIELDS)
            if query is not None and key[3] != query:
                continue
            try:
                window = row["window"].strip()
                start = date.fromisoformat(row["start_date"].strip())
                end = date.fromisoformat(row["end_date"].strip())
                clicks = int(row["clicks"])
                impressions = int(row["impressions"])
                position = float(row["position"]) if row["position"].strip() else None
                if not all(key) or window not in WINDOWS or end < start:
                    raise ValueError("invalid key, window label, or date range")
                if clicks < 0 or impressions < clicks:
                    raise ValueError("clicks must be nonnegative and at most impressions")
                if position is not None and (not math.isfinite(position) or position < 0):
                    raise ValueError("invalid average position")
                segment = dates.setdefault(key[:3], {})
                if segment.setdefault(window, (start, end)) != (start, end):
                    raise ValueError("rows in one segment and window must use the same dates")
                pair = pairs.setdefault(key, {})
                if window in pair:
                    raise ValueError("duplicate query, page, segment, and window")
                pair[window] = (clicks, impressions, position)
            except ValueError as error:
                raise ValueError(f"Line {reader.line_num}: {error}") from error

    if not pairs:
        raise ValueError("No rows match the requested query")
    for segment, windows in dates.items():
        if not all(window in windows for window in WINDOWS):
            continue
        prior_start, prior_end = windows["prior"]
        current_start, current_end = windows["current"]
        if prior_end >= current_start or prior_end - prior_start != current_end - current_start:
            raise ValueError(f"Use separate windows of equal length in {'/'.join(segment)}")
    return pairs


def display_metrics(row):
    if row is None:
        return ("", "", "", "")
    clicks, impressions, position = row
    ctr = f"{clicks / impressions:.2%}" if impressions else ""
    return (clicks, impressions, position, ctr)


def write_comparison(pairs):
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow([
        *KEY_FIELDS, "status",
        "prior_clicks", "prior_impressions", "prior_position", "prior_ctr",
        "current_clicks", "current_impressions", "current_position", "current_ctr",
        "ctr_change_percentage_points",
    ])
    for key, pair in sorted(pairs.items()):
        prior = pair.get("prior")
        current = pair.get("current")
        change = ""
        if prior is None:
            status = "missing_prior"
        elif current is None:
            status = "missing_current"
        elif not prior[1] or not current[1]:
            status = "zero_impressions"
        else:
            status = "paired"
            change = f"{100 * (current[0] / current[1] - prior[0] / prior[1]):+.2f}"
        writer.writerow([*key, status, *display_metrics(prior), *display_metrics(current), change])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--query", help="Compare rows for this exact query")
    args = parser.parse_args()
    try:
        write_comparison(read_pairs(args.csv_path, args.query))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
