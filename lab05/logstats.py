"""Модуль для разбора и статистики журнала сервиса."""

LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    """Разбирает строку журнала в словарь.

    Ожидаемый формат: «время уровень сообщение».
    Сообщение может содержать пробелы, поэтому строка делится
    не более чем на три части.

    :param line: строка журнала
    :return: {"time": ..., "level": ..., "message": ...}
    :raises ValueError: если строка пустая, содержит меньше трёх
        частей или уровень незнакомый
    """
    if not line or not line.strip():
        raise ValueError("пустая строка")

    parts = line.rstrip("\n").split(" ", 2)

    if len(parts) < 3:
        raise ValueError(f"недостаточно частей: {line!r}")

    time, level, message = parts

    if level not in LEVELS:
        raise ValueError(f"незнакомый уровень: {level!r}")

    return {"time": time, "level": level, "message": message}


def count_levels(lines) -> dict:
    """Считает количество строк каждого уровня.

    Испорченные строки считаются под ключом BROKEN.
    Пустые строки пропускаются.

    :param lines: последовательность строк (список или открытый файл)
    :return: словарь {уровень: количество}
    """
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
    """Возвращает n самых частых сообщений уровня ERROR.

    При равенстве частот сортировка по алфавиту.

    :param lines: последовательность строк
    :param n: сколько сообщений вернуть
    :return: список пар [сообщение, сколько раз]
    """
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
    """Формирует текст отчёта.

    :param counts: словарь {уровень: количество}
    :param errors: список пар [сообщение, сколько раз]
    :return: текст отчёта, заканчивающийся переводом строки
    """
    lines_out = ["Отчёт по журналу", ""]

    for level in sorted(counts):
        lines_out.append(f"{level}: {counts[level]}")

    lines_out.append("")
    lines_out.append("Частые ошибки:")

    for msg, cnt in errors:
        lines_out.append(f"- {msg} — {cnt}")

    return "\n".join(lines_out) + "\n"
