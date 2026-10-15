"""Основная программа: читает журнал и печатает отчёт."""

import sys

from stats import average_by_city, read_valid, warmest_city


def main():
    lines = sys.stdin.read().splitlines()
    non_empty = [line for line in lines if line.strip() != ""]

    records = read_valid(lines)

    parsed_count = len(records)
    skipped_count = len(non_empty) - parsed_count

    print(parsed_count)
    print(skipped_count)

    if records:
        best = warmest_city(records)
        averages = average_by_city(records)
        print(f"{averages[best]:.1f}")
    else:
        print("0.0")


if __name__ == "__main__":
    main()
