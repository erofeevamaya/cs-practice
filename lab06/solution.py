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
