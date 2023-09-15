import os


def to_port(num: int) -> int:
    return int(os.environ.get("PORT", num))


CLIENT_PORT = to_port(2000)
SERVER_PORT = to_port(3000)
DB_PORT = to_port(4000)

CLIENT_HOSTNAME = "localhost"
SERVER_HOSTNAME = "localhost"
DB_HOSTNAME = "localhost"

SECRET_KEY = "minecraft"
