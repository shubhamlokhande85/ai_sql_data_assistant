"""Generate and explain queries using Groq."""

from __future__ import annotations

import json
import re
from typing import Any

from groq_client import generate_response
from prompts import ANSWER_SYSTEM_PROMPT, SQL_SYSTEM_PROMPT

MAX_HISTORY_MESSAGES = 8
MAX_RESULT_ROWS_FOR_PROMPT = 100


def _recent_history(conversation_history: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {"role": message["role"], "content": message["content"][:4000]}
        for message in conversation_history[-MAX_HISTORY_MESSAGES:]
        if message.get("role") in {"user", "assistant"}
    ]


def _parse_json_response(response: str) -> dict[str, Any]:
    candidate = response.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate, flags=re.IGNORECASE)
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("The model response must be a JSON object.")
    if not isinstance(parsed.get("can_answer"), bool):
        raise ValueError("The model response is missing can_answer.")
    if not isinstance(parsed.get("sql", ""), str) or not isinstance(parsed.get("explanation", ""), str):
        raise ValueError("The model response has invalid fields.")
    return parsed


def generate_sql(
    user_question: str,
    schema: str,
    conversation_history: list[dict[str, str]],
) -> dict[str, Any]:
    """Ask Groq for one schema-grounded SQL statement as structured JSON."""
    messages = [{"role": "system", "content": SQL_SYSTEM_PROMPT}]
    messages.extend(_recent_history(conversation_history))
    messages.append(
        {
            "role": "user",
            "content": (
                f"Database schema:\n{schema}\n\n"
                f"Current question:\n{user_question}\n\n"
                "Return the required JSON object only."
            ),
        }
    )
    return _parse_json_response(generate_response(messages))


def generate_answer(
    user_question: str,
    sql: str,
    result_rows: list[dict[str, Any]],
    conversation_history: list[dict[str, str]],
) -> str:
    """Ask Groq to explain database rows without inventing values."""
    context = {
        "question": user_question,
        "sql": sql,
        "rows": result_rows[:MAX_RESULT_ROWS_FOR_PROMPT],
        "rows_included": min(len(result_rows), MAX_RESULT_ROWS_FOR_PROMPT),
        "total_rows": len(result_rows),
    }
    messages = [{"role": "system", "content": ANSWER_SYSTEM_PROMPT}]
    messages.extend(_recent_history(conversation_history))
    messages.append(
        {
            "role": "user",
            "content": "Explain these query results:\n" + json.dumps(context, default=str, ensure_ascii=True),
        }
    )
    return generate_response(messages)
