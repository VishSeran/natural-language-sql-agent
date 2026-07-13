# Natural Language SQL Agent 🗣️➡️🗄️

Query a MySQL database using plain English. This project uses **LangChain** and a **Hugging Face** LLM to translate natural language questions into SQL queries, execute them against a live database, and return human-readable answers — no SQL knowledge required.

## Overview

Extracting insights from a SQL database traditionally means writing SQL, joining tables by hand, and knowing the schema inside and out. This project removes that barrier by wrapping a MySQL database with a LangChain SQL agent powered by an open-source LLM from Hugging Face. Ask a question like *"Which country's customers spent the most?"* and get a direct answer, complete with the reasoning and the SQL query the agent generated along the way.

The example database used throughout is **Chinook**, a sample digital media store dataset with 11 tables (artists, albums, tracks, customers, invoices, employees, etc.) and 15,000+ records.

## Features

- **Natural language querying** — ask questions in everyday English instead of writing SQL
- **Automatic SQL generation** — the agent writes and executes the SQL for you
- **Schema-aware reasoning** — the agent inspects table structure before querying
- **Error recovery** — failed queries are retried automatically with corrected SQL
- **Command-line interface** — pass questions as CLI arguments for quick testing
- **Verbose mode** — see the agent's full reasoning chain, not just the final answer

## Tech Stack

- [LangChain](https://python.langchain.com/) — agent orchestration and SQL toolkit
- [langchain-huggingface](https://python.langchain.com/docs/integrations/llms/huggingface_pipelines/) — Hugging Face LLM integration
- **MySQL** — the target relational database
- `mysql-connector-python` — MySQL database driver

## Prerequisites

- Python 3.10+
- A running MySQL server
- A Hugging Face account/API token (if using the Hugging Face Inference API), or a local model if running inference locally

## Setup

### 1. Create a virtual environment

```bash
pip install virtualenv
virtualenv my_env
source my_env/bin/activate
```

### 2. Install dependencies

```bash
pip install langchain langchain-community langchain-huggingface \
    mysql-connector-python huggingface_hub
```

### 3. Set up the database

Create a MySQL server and load the Chinook sample database:

```bash
mysql --host=<host> --port=<port> --user=<user> --password=<password>
```

```sql
SOURCE chinook-mysql.sql;
```

Verify it loaded correctly:

```sql
USE Chinook;
SELECT COUNT(*) FROM Album;  -- should return 347
```

### 4. Configure environment variables

Create a `.env` file (or export these directly) with your database and Hugging Face credentials:

```
HUGGINGFACEHUB_API_TOKEN=your_hf_token
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=your_host
MYSQL_PORT=3306
MYSQL_DATABASE=Chinook
```

## Usage

Run a query directly from the command line:

```bash
python sql_agent.py --prompt "How many albums are there in the database?"
```

More examples:

```bash
python sql_agent.py --prompt "How many employees are there"
python sql_agent.py --prompt "Describe the PlaylistTrack table"
python sql_agent.py --prompt "Can you left join table Artist and table Album by ArtistId? Please show me 5 rows"
python sql_agent.py --prompt "Which country's customers spent the most by invoice?"
```

Each run prints the agent's reasoning steps (when `verbose=True`), the SQL it generated, and the final natural-language answer.

## How It Works

1. **LLM setup** — a Hugging Face model is loaded via `langchain-huggingface` and wrapped as a LangChain-compatible LLM.
2. **Database connection** — `SQLDatabase.from_uri()` connects to the MySQL instance using a standard connection URI.
3. **Agent creation** — `create_sql_agent()` builds a ReAct-style agent that can inspect the schema, write SQL, run it, and self-correct on errors.
4. **Query execution** — the agent takes a plain-English prompt, plans the necessary SQL steps, executes them, and returns a final answer.

## Project Structure

```
.
├── llm_agent.py       # Minimal script to test the Hugging Face LLM connection
├── sql_agent.py        # Full SQL agent with CLI prompt support
├── chinook-mysql.sql   # Sample database creation script
└── README.md
```

## Notes

- Replace all placeholder database credentials with your own before running.
- If you hit parsing errors from the agent, `handle_parsing_errors=True` will attempt to recover; press `Ctrl+C` and rerun if it gets stuck.
- Swap in any Hugging Face-hosted or local model by changing the model name/config in `llm_agent.py`.

## License

This project is licensed under the Apache 2.0 License.
