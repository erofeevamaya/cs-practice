from logstats import count_levels, top_errors, format_report


def main() -> None:
    path = input().strip()

    with open(path, encoding="utf-8") as log:
        counts = count_levels(log)

    with open(path, encoding="utf-8") as log:
        errors = top_errors(log, 3)

    total = sum(counts.values())
    error_count = counts.get("ERROR", 0)
    broken_count = counts.get("BROKEN", 0)

    print(total)
    print(error_count)
    print(broken_count)

    report = format_report(counts, errors)

    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report)


if __name__ == "__main__":
    main()
