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
    pass


def average_by_city(records: list[dict]) -> dict:
    """Средняя температура по каждому городу, округлённая до десятых."""
    pass


def warmest_city(records: list[dict]) -> str:
    """Город с наибольшей средней температурой."""
    pass
