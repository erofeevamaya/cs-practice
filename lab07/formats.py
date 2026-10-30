import json


def csv_to_records(text: str) -> list[dict]:
    """Разбирает CSV с заголовком в список словарей. Значения остаются строками."""
    lines = text.strip().split("\n")
    headers = lines[0].split(",")
    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = line.split(",")
        record = {}
        for i in range(len(headers)):
            record[headers[i]] = values[i]
        records.append(record)
    return records


def parse_settings(lines: list[str]) -> dict:
    """Простой YAML: «ключ: значение», списки через «- », комментарии после #."""
    result = {}
    current_list_key = None
    for line in lines:
        # отбрасываем комментарий
        if "#" in line:
            line = line[:line.index("#")]
        if not line.strip():
            continue

        # элемент списка
        if line.strip().startswith("- "):
            value = line.strip()[2:].strip()
            result[current_list_key].append(_convert_value(value))
            continue

        # пара ключ: значение
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            # открывается список
            current_list_key = key
            result[key] = []
        else:
            current_list_key = None
            result[key] = _convert_value(value)

    return result


def _convert_value(value: str):
    """Приводит строку к числу/булеву значению, если это возможно."""
    if value == "true" or value == "yes":
        return True
    if value == "false" or value == "no":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из словаря по значению ключа key."""
    result = []
    for row in rows:
        merged = {}
        row_key = row.get(key)
        if row_key in extra:
            # сначала данные из справочника, потом данные записи (они важнее)
            for k, v in extra[row_key].items():
                merged[k] = v
        for k, v in row.items():
            merged[k] = v
        result.append(merged)
    return result


def records_to_json(records: list[dict]) -> str:
    """Список словарей в JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)import json


def csv_to_records(text: str) -> list[dict]:
    """Разбирает CSV с заголовком в список словарей. Значения остаются строками."""
    if not text or not text.strip():
        return []

    lines = text.strip().split("\n")
    headers = [h.strip() for h in lines[0].split(",")]

    records = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(",")]
        record = {}
        for i in range(len(headers)):
            record[headers[i]] = values[i]
        records.append(record)
    return records


def parse_settings(lines: list[str]) -> dict:
    """Простой YAML: «ключ: значение», списки через «- », комментарии после #."""
    result = {}
    current_list_key = None

    for line in lines:
        # отбрасываем комментарий
        if "#" in line:
            line = line[:line.index("#")]
        if not line.strip():
            continue

        # элемент списка
        if line.strip().startswith("- "):
            value = line.strip()[2:].strip()
            result[current_list_key].append(_convert_value(value))
            continue

        # пара ключ: значение
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            # открывается список
            current_list_key = key
            result[key] = []
        else:
            current_list_key = None
            result[key] = _convert_value(value)

    return result


def _convert_value(value: str):
    """Приводит строку к числу/булеву значению, если это возможно."""
    if value in ("true", "yes"):
        return True
    if value in ("false", "no"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из словаря по значению ключа key."""
    result = []
    for row in rows:
        merged = {}
        row_key = row.get(key)
        if row_key in extra:
            # сначала данные из справочника
            for k, v in extra[row_key].items():
                merged[k] = v
        # потом данные записи (они важнее)
        for k, v in row.items():
            merged[k] = v
        result.append(merged)
    return result


def records_to_json(records: list[dict]) -> str:
    """Список словарей в JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
