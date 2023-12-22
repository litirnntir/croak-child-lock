import json


def update_json(file: str, key: str, value: any) -> None:
    """
    Обновляет данные в JSON-файле по заданному ключу и значению.

    Параметры:
    file: имя JSON-файла, который нужно обновить
    key: ключ, по которому нужно обновить значение
    value: новое значение, которое нужно записать по ключу

    Возвращает:
    None
    """
    with open(file, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(file, "w") as f:
        json.dump(data, f)
