import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

def get_required_env(name):
    value = os.getenv(name)

    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def get_db_port():
    raw_port = os.getenv("DB_PORT", "3306")

    try:
        return int(raw_port)
    except ValueError as error:
        raise RuntimeError("DB_PORT must be an integer.") from error


def get_connection():
    return mysql.connector.connect(
        host=get_required_env("DB_HOST"),
        port=get_db_port(),
        database=get_required_env("DB_NAME"),
        user=get_required_env("DB_USER"),
        password=get_required_env("DB_PASSWORD"),
    )


if __name__ == "__main__":
    connection = get_connection()

    if connection.is_connected():
        print("Conexión MySQL correcta")

    connection.close()
