# AI SQL Data Assistant

A Streamlit chatbot that turns natural-language questions into read-only MySQL queries with Groq, validates each query, runs it with a hard row limit, and explains the returned data. Conversation context is kept in Streamlit session state so users can ask follow-up questions.

## Architecture

- `app.py` renders the chat, connection status, SQL, result tables, and optional charts.
- `database.py` opens MySQL connections, discovers the schema through `information_schema`, and executes approved queries in read-only transactions.
- `groq_client.py` provides the configured Groq SDK client and handles API failures.
- `prompts.py` defines the SQL-generation and result-explanation instructions.
- `sql_generator.py` builds bounded conversation context and parses the model's JSON response.
- `sql_validator.py` parses MySQL SQL, rejects comments and non-SELECT statements, and enforces a 500-row maximum.

The application never uses the OpenAI API. Use a dedicated MySQL account with only `SELECT` permission, even though generated SQL is validated before execution.

## Requirements

- Python 3.10 or newer
- A MySQL server and database
- A Groq API key

## MySQL Setup

Create or select the database and create a dedicated account. Run these statements as a MySQL administrator, replacing the database, host, and password with your own values:

```sql
CREATE USER 'sql_chatbot_readonly'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT SELECT ON `your_database`.* TO 'sql_chatbot_readonly'@'localhost';
```

Use the narrowest host permitted by your deployment. If the app runs on a different host, replace `localhost` with that host or an appropriately restricted network range. Do not grant write, file, or administrative privileges.

## Groq API Key

Create an API key in your Groq account. Keep it private and store it only in the local `.env` file or a deployment secret manager. Never commit `.env` or paste the key into source code.

## Configure Environment

From the project directory, create a local `.env` based on `.env.example` and set the values:

```dotenv
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=qwen/qwen3.8-27b
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=sql_chatbot_readonly
DB_PASSWORD=your-read-only-password
DB_NAME=your_database
```

The default model can be changed with `GROQ_MODEL` if your account uses another currently available Groq model. Do not commit `.env`.

## Install and Run

Run these commands from the `sql_chatbot` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` and copy the example with `cp .env.example .env`. Edit `.env` with your credentials before starting the app.

## Example Questions

- How many customers do we have?
- Show the top 10 customers by sales.
- What was the total revenue last month?
- Which city has the highest sales?
- Show sales by month.
- How many orders were cancelled?
- What is the average order value?
- Show customers who have never placed an order.
- Compare this month's sales with last month's sales.
- Which product generated the highest revenue?

The available questions depend on the actual tables and columns discovered in your database. Follow-up questions can refer to recent messages in the same Streamlit session.

## Security Considerations

- Store Groq and database credentials in environment variables; never hard-code or display them.
- Use a dedicated MySQL account with only `SELECT` privileges and restrict its network access.
- SQL is parsed as MySQL, and only one SELECT statement is accepted. Comments, SELECT INTO, and locking reads are rejected.
- Every accepted query is rewritten with a maximum of 500 returned rows and executed in a read-only transaction.
- Only a bounded number of recent chat messages and up to 100 result rows are sent to Groq for context. Avoid sending sensitive or regulated data to an external model unless your organization's policies permit it.
- Database and API failures are shown as friendly messages; internal exceptions and credentials are not rendered in the UI.
- This validation is defense in depth, not a substitute for database permissions, network controls, and careful handling of sensitive data.
