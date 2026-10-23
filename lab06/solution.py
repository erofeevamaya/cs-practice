python
def count_by_extension(paths: list[str]) -> dict[str, int]:
    result = {}
    for path in paths:
        name = path.split("/")[-1]  # берём только имя файла
        if "." in name:
            ext = name.split(".")[-1].lower()
        else:
            ext = ""
        result[ext] = result.get(ext, 0) + 1
    return result

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    # сортируем по алфавиту, потом ищем максимальную вложенность
    best = sorted(paths)[0]
    for path in sorted(paths):
        if path.count("/") > best.count("/"):
            best = path
    return best


def human_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} Б"
    units = ["КБ", "МБ", "ГБ", "ТБ"]
    size = n_bytes / 1024
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.1f} {units[i]}"
