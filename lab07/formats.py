"""Практика: перевод между форматами CSV, JSON, YAML."""

import json


def csv_to_records(text: str) -> list[dict]:
    """Разбирает CSV с заголовком в список словарей.

    Значения остаются строками. Разделитель — запятая,
    первая непустая строка — заголовок.
    """
    lines = text.splitlines()
    # Отбрасываем пустые строки (например, хвостовой перевод строки)
    lines = [line for line in lines if line.strip() != ""]
    if not lines:
        return []

    header = lines[0].split(",")
    records = []
    for line in lines[1:]:
        values = line.split(",")
        records.append(dict(zip(header, values)))
    return records


def _parse_scalar(value: str):
    """Приводит строковое значение к нужному типу (учебный YAML)."""
    value = value.strip()
    if value == "":
        return ""
    lowered = value.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    # Числа: сначала пробуем целое, потом дробное
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def parse_settings(lines: list[str]) -> dict:
    """Разбирает учебное подмножество YAML в словарь.

    Поддерживает:
      * комментарии после #;
      * пары «ключ: значение» с приведением типов;
      * списки: «ключ:» без значения и элементы «- значение».
    Вложенность не поддерживается.
    """
    result: dict = {}
    current_list_key = None  # ключ, для которого сейчас собирается список

    for raw_line in lines:
        # Убираем комментарий (всё после #)
        line = raw_line.split("#", 1)[0]
        if line.strip() == "":
            continue

        stripped = line.strip()

        # Элемент списка
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if current_list_key is not None:
                result[current_list_key].append(_parse_scalar(item))
            continue
        elif stripped == "-":
            if current_list_key is not None:
                result[current_list_key].append("")
            continue

        # Пара «ключ: значение» или открытие списка
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "":
                # Открывается список
                result[key] = []
                current_list_key = key
            else:
                result[key] = _parse_scalar(value)
                current_list_key = None

    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из справочника extra по значению ключа key.

    Поля самой записи важнее: при конфликте остаётся значение из записи.
    Записи без пары в справочнике остаются как есть.
    """
    merged = []
    for row in rows:
        new_row = dict(row)  # копия, чтобы не мутировать исходные данные
        row_key = str(row.get(key))
        if row_key in extra:
            # Поля справочника добавляем, но не перезаписываем существующие
            for field, value in extra[row_key].items():
                if field not in new_row:
                    new_row[field] = value
        merged.append(new_row)
    return merged


def records_to_json(records: list[dict]) -> str:
    """Список словарей в JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
