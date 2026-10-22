"""Модуль для разбора и статистики журнала сервиса."""

LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> dict:
    """Разбирает строку журнала в словарь.
    
    Негодная строка вызывает ValueError.
    """
    # 1. Если строка пустая (или состоит из пробелов) — сразу ошибка
    if not line or not line.strip():
        raise ValueError("пустая строка")

    # 2. Убираем ТОЛЬКО перевод строки в конце (\n), 
    # начальные пробелы не трогаем — если они есть, это ошибка
    clean_line = line.rstrip("\n")

    # 3. Разбиваем максимум на 3 части
    parts = clean_line.split(" ", 2)

    # 4. Частей должно быть ровно 3 (время, уровень, сообщение)
    if len(parts) != 3:
        raise ValueError(f"неверное количество частей: {line!r}")

    # 5. Распаковываем
    time, level, message = parts

    # 6. Проверяем уровень строго по списку
    if level not in LEVELS:
        raise ValueError(f"незнакомый уровень: {level!r}")

    # 7. Проверяем, что время и сообщение не пустые (например, если были лишние пробелы)
    if not time:
        raise ValueError(f"пустое время: {line!r}")
    if not message:
        raise ValueError(f"пустое сообщение: {line!r}")

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
