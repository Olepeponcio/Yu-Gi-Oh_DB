import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

LOCAL_DB_HOSTS = {"localhost", "127.0.0.1", "::1"}


def get_required_env(name):
    value = os.getenv(name)

    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


def get_db_host():
    host = get_required_env("DB_HOST")
    allow_remote = os.getenv("DB_ALLOW_REMOTE_DB", "").lower() in {"1", "true", "yes"}

    if host not in LOCAL_DB_HOSTS and not allow_remote:
        raise RuntimeError(
            "DB_HOST must be local unless DB_ALLOW_REMOTE_DB=true is explicitly set."
        )

    return host


def get_db_port():
    raw_port = os.getenv("DB_PORT", "3306")

    try:
        return int(raw_port)
    except ValueError as error:
        raise RuntimeError("DB_PORT must be an integer.") from error


def get_db_user():
    user = get_required_env("DB_USER")

    if user.lower() == "root":
        raise RuntimeError("DB_USER must not be root for ETL loads.")

    return user


def get_connection():
    return mysql.connector.connect(
        host=get_db_host(),
        port=get_db_port(),
        database=get_required_env("DB_NAME"),
        user=get_db_user(),
        password=get_required_env("DB_PASSWORD"),
    )


if __name__ == "__main__":
    connection = get_connection()

    if connection.is_connected():
        print("Conexión MySQL correcta")

    connection.close()
