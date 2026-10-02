"""MySQL access and dynamic schema discovery."""

from __future__ import annotations

import os
from typing import Any

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from mysql.connector import Error as MySQLError

load_dotenv()


class DatabaseError(RuntimeError):
    """A safe-to-display database operation error."""


def _connection_options() -> dict[str, Any]:
    required = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise DatabaseError(
            "Database configuration is incomplete. Set: " + ", ".join(missing)
        )

    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError as exc:
        raise DatabaseError("DB_PORT must be a valid port number.") from exc

    return {
        "host": os.environ["DB_HOST"],
        "port": port,
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_NAME"],
        "connection_timeout": 10,
    }


def get_connection() -> mysql.connector.MySQLConnection:
    """Open a new connection without exposing credentials in errors."""
    try:
        return mysql.connector.connect(**_connection_options())
    except DatabaseError:
        raise
    except MySQLError as exc:
        raise DatabaseError("Could not connect to the configured MySQL database.") from exc


def test_database_connection() -> tuple[bool, str]:
    """Return connection status and a friendly diagnostic."""
    connection = None
    try:
        connection = get_connection()
        return True, "Connected"
    except DatabaseError as exc:
        return False, str(exc)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def get_table_names() -> list[str]:
    """Return table names in the configured database."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT TABLE_NAME FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE' "
            "ORDER BY TABLE_NAME",
            (os.environ["DB_NAME"],),
        )
        return [row[0] for row in cursor.fetchall()]
    except MySQLError as exc:
        raise DatabaseError("Could not retrieve database tables.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_database_schema() -> str:
    """Discover tables and columns from information_schema at runtime."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE "
            "FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = %s "
            "ORDER BY TABLE_NAME, ORDINAL_POSITION",
            (os.environ["DB_NAME"],),
        )
        rows = cursor.fetchall()
    except MySQLError as exc:
        raise DatabaseError("Could not retrieve the database schema.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    if not rows:
        return f"Database: {os.environ['DB_NAME']}\n\nNo tables were found."

    tables: dict[str, list[str]] = {}
    for table_name, column_name, column_type in rows:
        tables.setdefault(table_name, []).append(f"- {column_name} {column_type}")

    lines = [f"Database: {os.environ['DB_NAME']}", "", "Tables:"]
    for table_name, columns in tables.items():
        lines.extend(("", f"{table_name}:", *columns))
    return "\n".join(lines)


def execute_select_query(sql: str) -> pd.DataFrame:
    """Execute SQL already approved by sql_validator and return its rows."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        connection.start_transaction(readonly=True)
        cursor = connection.cursor()
        cursor.execute(sql)
        column_names = [item[0] for item in cursor.description or ()]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=column_names)
    except MySQLError as exc:
        raise DatabaseError("The database could not run that query.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            try:
                connection.rollback()
            finally:
                connection.close()
