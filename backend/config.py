import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "mysql54878978"),
    "database": os.environ.get("DB_NAME", "movahub"),
}

HOST = "localhost"
PORT = 8000
SESSAO_DURACAO = 60 * 60  # 1 hora, em segundos