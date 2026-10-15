"""Модуль обработки записей метеостанции."""


def parse_record(line: str) -> dict:
    """Разбирает строку 'город;температура;дата' в словарь.

    Если строка негодная — возбуждает ValueError.
    """
    parts = line.split(";")

    if len(parts) != 3:
        raise ValueError(f"Ожидалось 3 поля, получено {len(parts)}: {line!r}")

    city, temp_str, date = parts

    if city.strip() == "":
        raise ValueError(f"Пустое название города: {line!r}")
    if date.strip() == "":
        raise ValueError(f"Пустая дата: {line!r}")

    try:
        temperature = float(temp_str)
    except ValueError:
        raise ValueError(f"Температура не число: {temp_str!r}")

    return {"city": city, "temperature": temperature, "date": date}

def read_valid(lines: list[str]) -> list[dict]:
    """Разбирает строки журнала, пропуская пустые и негодные."""
    records = []
    for line in lines:
        if line.strip() == "":
            continue
        try:
            records.append(parse_record(line))
        except ValueError:
            continue
    return records

def average_by_city(records: list[dict]) -> dict:
    """Средняя температура по каждому городу, округлённая до десятых."""
    total = {}
    count = {}

    for rec in records:
        city = rec["city"]
        total[city] = total.get(city, 0) + rec["temperature"]
        count[city] = count.get(city, 0) + 1

    averages = {}
    for city in total:
        averages[city] = round(total[city] / count[city], 1)
    return averages


def warmest_city(records: list[dict]) -> str:
    """Город с наибольшей средней температурой.

    При равенстве — первый по алфавиту.
    """
    if not records:
        raise ValueError("Нет записей для анализа")

    averages = average_by_city(records)

    best_city = None
    best_temp = None
    for city in sorted(averages):
        temp = averages[city]
        if best_temp is None or temp > best_temp:
            best_temp = temp
            best_city = city
    return best_city
