"""Reusable Groq chat-completion client."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, APITimeoutError, Groq

load_dotenv()

DEFAULT_MODEL = "qwen/qwen3.8-27b"


class GroqRequestError(RuntimeError):
    """A friendly error raised for Groq request failures."""


def generate_response(messages: list[dict[str, str]]) -> str:
    """Send chat messages to Groq and return the assistant response."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise GroqRequestError("GROQ_API_KEY is not configured.")

    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    try:
        client = Groq(api_key=api_key, timeout=30.0, max_retries=1)
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
        )
        content = completion.choices[0].message.content
        if not content:
            raise GroqRequestError("Groq returned an empty response.")
        return content.strip()
    except GroqRequestError:
        raise
    except APITimeoutError as exc:
        raise GroqRequestError("The Groq request timed out. Please try again.") from exc
    except APIConnectionError as exc:
        raise GroqRequestError("Could not connect to Groq. Please try again.") from exc
    except APIStatusError as exc:
        raise GroqRequestError("Groq could not process the request. Check the model and API access.") from exc
    except Exception as exc:
        raise GroqRequestError("Groq returned an unexpected response.") from exc
