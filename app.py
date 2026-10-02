"""Streamlit interface for the AI SQL Data Assistant."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from database import DatabaseError, execute_select_query, get_database_schema, test_database_connection
from groq_client import GroqRequestError
from sql_generator import generate_answer, generate_sql
from sql_validator import apply_row_limit, validate_sql

MAX_HISTORY_MESSAGES = 8


@st.cache_data(ttl=20, show_spinner=False)
def _connection_status() -> tuple[bool, str]:
    return test_database_connection()


def _display_turns() -> None:
    for turn_index, turn in enumerate(st.session_state.turns):
        with st.chat_message("user"):
            st.markdown(turn["question"])
        with st.chat_message("assistant"):
            st.markdown(turn["answer"])
            if turn.get("sql"):
                with st.expander("Generated SQL"):
                    st.code(turn["sql"], language="sql")
            result = turn.get("result")
            if result is not None:
                with st.expander("Query Result", expanded=True):
                    st.dataframe(result, use_container_width=True, hide_index=True)
                    _chart_controls(result, turn_index)


def _chart_controls(result: pd.DataFrame, turn_index: int) -> None:
    if result.empty or len(result) < 2:
        return

    numeric_columns = result.select_dtypes(include="number").columns.tolist()
    category_columns = [column for column in result.columns if column not in numeric_columns]

    chart_options: list[str] = []
    if numeric_columns and category_columns:
        chart_options.extend(("Bar", "Line", "Area", "Pie"))
    if len(numeric_columns) >= 2:
        chart_options.append("Scatter")
    if numeric_columns:
        chart_options.extend(("Histogram", "Box"))
    elif category_columns:
        chart_options.append("Count")
    if not chart_options:
        return

    default_chart = "Bar" if category_columns and numeric_columns else chart_options[0]
    if not st.checkbox(
        "Show visualization",
        value=True,
        key=f"chart_enabled_{turn_index}",
    ):
        return

    selected_chart = st.selectbox(
        "Chart type",
        chart_options,
        index=chart_options.index(default_chart),
        key=f"chart_type_{turn_index}",
    )

    figure = None
    if selected_chart in {"Bar", "Line", "Area", "Pie"}:
        x_column = st.selectbox(
            "Category or date",
            category_columns,
            key=f"chart_x_{turn_index}",
        )
        y_column = st.selectbox(
            "Value",
            numeric_columns,
            key=f"chart_y_{turn_index}",
        )
        if selected_chart == "Pie":
            figure = px.pie(result, names=x_column, values=y_column)
        else:
            color_columns = [column for column in category_columns if column != x_column]
            color_column = st.selectbox(
                "Group by (optional)",
                [None, *color_columns],
                format_func=lambda column: "None" if column is None else str(column),
                key=f"chart_color_{turn_index}",
            )
            chart_builder = {
                "Bar": px.bar,
                "Line": px.line,
                "Area": px.area,
            }[selected_chart]
            chart_options = {"x": x_column, "y": y_column, "color": color_column}
            if selected_chart == "Line":
                chart_options["markers"] = True
            figure = chart_builder(result, **chart_options)
    elif selected_chart == "Scatter":
        x_column, y_column = st.columns(2)
        x_value = x_column.selectbox(
            "X value",
            numeric_columns,
            key=f"chart_x_{turn_index}",
        )
        y_defaults = [column for column in numeric_columns if column != x_value]
        if not y_defaults:
            y_defaults = numeric_columns
        y_value = y_column.selectbox(
            "Y value",
            y_defaults,
            key=f"chart_y_{turn_index}",
        )
        color_column = st.selectbox(
            "Group by (optional)",
            [None, *category_columns],
            format_func=lambda column: "None" if column is None else str(column),
            key=f"chart_color_{turn_index}",
        )
        figure = px.scatter(result, x=x_value, y=y_value, color=color_column)
    elif selected_chart == "Histogram":
        value_column = st.selectbox(
            "Value",
            numeric_columns,
            key=f"chart_value_{turn_index}",
        )
        figure = px.histogram(result, x=value_column)
    elif selected_chart == "Box":
        value_column = st.selectbox(
            "Value",
            numeric_columns,
            key=f"chart_value_{turn_index}",
        )
        category_column = st.selectbox(
            "Group by (optional)",
            [None, *category_columns],
            format_func=lambda column: "None" if column is None else str(column),
            key=f"chart_color_{turn_index}",
        )
        figure = px.box(result, x=category_column, y=value_column)
    else:
        category_column = st.selectbox(
            "Category",
            category_columns,
            key=f"chart_x_{turn_index}",
        )
        figure = px.histogram(result, x=category_column)

    if figure is not None:
        figure.update_layout(height=420, margin=dict(l=16, r=16, t=40, b=16))
        st.plotly_chart(figure, use_container_width=True, key=f"chart_{turn_index}")


def _answer_question(question: str) -> dict[str, object]:
    history = st.session_state.history[-MAX_HISTORY_MESSAGES:]
    schema = get_database_schema()
    generated = generate_sql(question, schema, history)

    if not generated["can_answer"]:
        explanation = generated["explanation"] or "The available database schema is not enough to answer that."
        return {"question": question, "answer": explanation, "sql": "", "result": None}

    sql = generated["sql"].strip()
    validation = validate_sql(sql)
    if not validation["valid"]:
        return {
            "question": question,
            "answer": "I couldn't safely run the generated query. Please rephrase the question and try again.",
            "sql": sql,
            "result": None,
        }

    safe_sql = apply_row_limit(sql)
    result = execute_select_query(safe_sql)
    rows = result.to_dict(orient="records")
    answer = generate_answer(question, safe_sql, rows, history)
    return {"question": question, "answer": answer, "sql": safe_sql, "result": result}


def main() -> None:
    st.set_page_config(page_title="AI SQL Data Assistant", page_icon=":speech_balloon:", layout="wide")
    st.title("AI SQL Data Assistant")

    if "turns" not in st.session_state:
        st.session_state.turns = []
    if "history" not in st.session_state:
        st.session_state.history = []

    with st.sidebar:
        st.subheader("Database")
        connected, status = _connection_status()
        if connected:
            st.success("Connected")
        else:
            st.error(status)
        if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
            st.session_state.turns = []
            st.session_state.history = []
            st.rerun()

    _display_turns()
    question = st.chat_input("Ask a question about your database")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Checking the schema and preparing a safe query..."):
            try:
                turn = _answer_question(question)
            except DatabaseError as exc:
                turn = {
                    "question": question,
                    "answer": str(exc),
                    "sql": "",
                    "result": None,
                }
            except GroqRequestError as exc:
                turn = {
                    "question": question,
                    "answer": str(exc),
                    "sql": "",
                    "result": None,
                }
            except (ValueError, TypeError):
                turn = {
                    "question": question,
                    "answer": "Sorry, I couldn't interpret a safe query for that request. Please try rephrasing it.",
                    "sql": "",
                    "result": None,
                }
            except Exception:
                turn = {
                    "question": question,
                    "answer": "Something went wrong while processing that question. Please try again.",
                    "sql": "",
                    "result": None,
                }

        st.markdown(str(turn["answer"]))
        if turn.get("sql"):
            with st.expander("Generated SQL"):
                st.code(str(turn["sql"]), language="sql")
        result = turn.get("result")
        if isinstance(result, pd.DataFrame):
            with st.expander("Query Result", expanded=True):
                st.dataframe(result, use_container_width=True, hide_index=True)
                _chart_controls(result, len(st.session_state.turns))

    st.session_state.turns.append(turn)
    st.session_state.history.extend(
        [
            {"role": "user", "content": question},
            {"role": "assistant", "content": str(turn["answer"])},
        ]
    )
    st.session_state.history = st.session_state.history[-MAX_HISTORY_MESSAGES:]


if __name__ == "__main__":
    main()
