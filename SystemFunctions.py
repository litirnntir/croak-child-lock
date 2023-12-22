import base64
import json

from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# with open("key.key", "wb") as file:
#     file.write(key)

with open("key.key", "rb") as file:
    key = file.read()

fernet = Fernet(key)


def encrypt_json(filename):
    with open(filename, "rb") as file:
        data = file.read()
    encrypted_data = fernet.encrypt(data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt_json(filename):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")


def update_json(filename, key, value):
    data = json.loads(decrypt_json(filename))
    data[key] = value
    # dict -> json -> bytes
    data = json.dumps(data)
    bytes_obj = data.encode('utf-8')
    encrypted_data = fernet.encrypt(bytes_obj)
    print(data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


update_json("test.json", "total", 10)

# encrypt_json("test.json")

# a = json.loads(decrypt_json("test.json"))
# with open("test.json", "w") as f:
#     json.dump(a, f)
