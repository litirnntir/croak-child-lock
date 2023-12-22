import json

from cryptography.fernet import Fernet

with open("key.key", "rb") as file:
    key = file.read()

fernet = Fernet(key)


def encrypt_json(filename: str) -> None:
    """Шифрует содержимое JSON-файла с помощью ключа fernet.

    :param filename: имя JSON-файла для шифрования
    """
    with open(filename, "rb") as file:
        data = file.read()
    encrypted_data = fernet.encrypt(data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt_json(filename: str) -> str:
    """Расшифровывает содержимое JSON-файла с помощью ключа fernet.

    :param filename: имя JSON-файла для расшифровки
    :return: расшифрованное содержимое JSON-файла в виде строки
    """
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")


def update_json(filename: str, key: str, value: any) -> None:
    """Обновляет значение по ключу в JSON-файле и шифрует его с помощью ключа fernet.

    :param filename: имя JSON-файла для обновления
    :param key: ключ, по которому нужно обновить значение
    :param value: новое значение для ключа
    """
    data = json.loads(decrypt_json(filename))
    data[key] = value
    # dict -> json -> bytes
    data = json.dumps(data)
    bytes_obj = data.encode('utf-8')
    encrypted_data = fernet.encrypt(bytes_obj)
    print(data)
    with open(filename, "wb") as f:
        f.write(encrypted_data)


update_json("test.json", "total", 10)
