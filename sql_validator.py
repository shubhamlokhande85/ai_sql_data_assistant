"""Fail-closed validation and row limiting for generated SQL."""

from __future__ import annotations

import re
from typing import Any

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

MAX_ROWS = 500
_ALLOWED_ROOTS = (exp.Select, exp.Union, exp.Intersect, exp.Except)


def _contains_comment(sql: str) -> bool:
    """Detect SQL comments outside string literals and quoted identifiers."""
    quote: str | None = None
    index = 0
    while index < len(sql):
        character = sql[index]
        if quote:
            if character == "\\":
                index += 2
                continue
            if character == quote:
                if index + 1 < len(sql) and sql[index + 1] == quote:
                    index += 2
                    continue
                quote = None
        elif character in ("'", '"', "`"):
            quote = character
        elif sql.startswith("--", index) or character == "#":
            return True
        elif sql.startswith("/*", index) or sql.startswith("*/", index):
            return True
        index += 1
    return False


def _parse_select(sql: str) -> tuple[exp.Expression | None, str | None]:
    if not isinstance(sql, str) or not sql.strip():
        return None, "The generated SQL is empty."
    if _contains_comment(sql):
        return None, "SQL comments are not allowed."

    try:
        statements = sqlglot.parse(sql, read="mysql")
    except ParseError:
        return None, "The generated SQL is not valid MySQL syntax."

    if len(statements) != 1 or statements[0] is None:
        return None, "Only one SQL statement is allowed."

    statement = statements[0]
    if not isinstance(statement, _ALLOWED_ROOTS):
        return None, "Only SELECT queries are allowed."

    into_expression = getattr(exp, "Into", None)
    if into_expression is not None and any(statement.find_all(into_expression)):
        return None, "SELECT INTO statements are not allowed."

    # Locking reads are not needed for analytics and must not bypass read-only intent.
    if re.search(r"\bFOR\s+UPDATE\b|\bLOCK\s+IN\s+SHARE\s+MODE\b", sql, re.IGNORECASE):
        return None, "Locking SELECT queries are not allowed."

    return statement, None


def validate_sql(sql: str) -> dict[str, Any]:
    """Return whether SQL is a single non-mutating SELECT statement."""
    _, reason = _parse_select(sql)
    if reason:
        return {"valid": False, "reason": reason}
    return {"valid": True, "reason": "Query is a single SELECT statement."}


def apply_row_limit(sql: str) -> str:
    """Return validated SQL with a hard maximum result-row limit."""
    statement, reason = _parse_select(sql)
    if reason or statement is None:
        raise ValueError(reason or "The generated SQL could not be validated.")
    statement.set("limit", exp.Limit(expression=exp.Literal.number(MAX_ROWS)))
    return statement.sql(dialect="mysql")
