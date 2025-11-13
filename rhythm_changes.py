#!/usr/bin/env python3
"""
Generate random 16-row "sets" from a CSV of chord permutations.

Usage examples:

    python rhythm_changes.py permutations.csv

    python rhythm_changes.py "Rhythm Changes Permutations - First 8 - All Permutations.csv" --sets 3 --size 16

Options:
    --sets N   = number of random sets to generate (default: 1)
    --size N   = number of rows per set (default: 16)
    --seed N   = random seed for reproducibility (optional)
"""

import csv
import random
import argparse
from typing import List, Tuple


def load_rows(csv_path: str) -> Tuple[List[str], List[List[str]]]:
    """Load header and rows from a UTF-8 CSV file."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # first row is header
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    return header, rows


def generate_set(rows: List[List[str]], size: int = 16) -> List[List[str]]:
    """Return one random set (sample) of `size` unique rows."""
    if size > len(rows):
        raise ValueError(f"Requested size {size} is larger than total rows {len(rows)}.")
    return random.sample(rows, size)


def format_set(set_index: int, header: List[str], rows: List[List[str]]) -> str:
    """Format one set as a nice aligned text table."""
    # Determine column widths
    num_cols = len(header)
    col_widths = []

    for col in range(num_cols):
        max_len = len(header[col])
        for row in rows:
            if col < len(row):
                max_len = max(max_len, len(str(row[col])))
        col_widths.append(max_len)

    def fmt_cell(text: str, width: int) -> str:
        return text.ljust(width)

    lines = []
    lines.append(f"========== First 8 Bars of Rhythm Changes (Permutations) {set_index} ==========")

    # Header row
    header_cells = [fmt_cell(h, col_widths[i]) for i, h in enumerate(header)]
    header_line = "Row | " + " | ".join(header_cells)
    lines.append(header_line)

    # Separator
    sep = "-" * len(header_line)
    lines.append(sep)

    # Data rows
    for i, row in enumerate(rows, start=1):
        cells = []
        for col in range(num_cols):
            value = row[col] if col < len(row) else ""
            cells.append(fmt_cell(str(value), col_widths[col]))
        line = str(i).rjust(3) + " | " + " | ".join(cells)
        lines.append(line)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate random 16-row sets from a chord permutation CSV."
    )
    parser.add_argument(
        "--sets",
        type=int,
        default=1,
        help="Number of random sets to generate (default: 1)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=16,
        help="Number of rows per set (default: 16)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible output",
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    header, rows = load_rows("Rhythm Changes Permutations - First 8 - All Permutations.csv")


    for i in range(1, args.sets + 1):
        sample_rows = generate_set(rows, size=args.size)
        print(format_set(i, header, sample_rows))
        print()  # blank line between sets


if __name__ == "__main__":
    main()
