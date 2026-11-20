"""Модуль для разбора и статистики журнала сервиса."""

LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
        if not line or not line.strip():
        raise ValueError("пустая строка")

        
    clean_line = line.strip() 
    parts = clean_line.split(" ", 2)

   ообщение.
    if len(parts) < 3:
        raise ValueError(f"недостаточно частей в строке: {line!r}")

    time, level, message = parts

    if level not in LEVELS:
        raise ValueError(f"незнакомый уровень: {level!r}")

    # 6. Возвращаемreturn {"time": time, "level": level, "message": message}


def count_levels(lines) -> dict:
  
    counts: dict = {}

    for line in lines:
        if not line or not line.strip():
            continue
        try:
            event = parse_event(line)
            level = event["level"]
        except ValueError:
            level = "BROKEN"
        counts[level] = counts.get(level, 0) + 1

    return counts


def top_errors(lines, n: int) -> list:
    counter: dict = {}

    for line in lines:
        if not line or not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue
        if event["level"] == "ERROR":
            msg = event["message"]
            counter[msg] = counter.get(msg, 0) + 1

    ordered = sorted(counter.items(), key=lambda item: (-item[1], item[0]))

    return [[msg, cnt] for msg, cnt in ordered[:n]]


def format_report(counts: dict, errors: list) -> str:
    lines_out = ["Отчёт по журналу", ""]

    for level in sorted(counts):
        lines_out.append(f"{level}: {counts[level]}")

    lines_out.append("")
    lines_out.append("Частые ошибки:")

    for msg, cnt in errors:
        lines_out.append(f"- {msg} — {cnt}")

    return "\n".join(lines_out) + "\n"
