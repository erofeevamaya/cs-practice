def count_by_extension(paths: list[str]) -> dict[str, int]:
    counts = {}
    for path in paths:
        name = path.rsplit("/", 1)[-1]
        # Расширения нет, если:
        # 1) точки нет вообще ("Makefile")
        # 2) имя начинается с точки (скрытые файлы: ".gitignore", ".gitig")
        # 3) после последней точки пусто ("file.")
        if "." in name and not name.startswith(".") and name.rsplit(".", 1)[-1]:
            ext = name.rsplit(".", 1)[-1].lower()
        else:
            ext = ""
        counts[ext] = counts.get(ext, 0) + 1
    return counts


def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return min(paths, key=lambda p: (-p.count("/"), p))


def human_size(n_bytes: int) -> str:
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    size = float(n_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{int(size)} {unit}" if unit == "Б" else f"{size:.1f} {unit}"
        size /= 1024
