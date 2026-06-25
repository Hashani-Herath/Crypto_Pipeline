# Automated Crypto Market Data Pipeline (Local ETL Architecture)

## 📌 Project Overview
This project implements a local, fully automated **ETL (Extract, Transform, Load)** data pipeline designed to capture, clean, and store historical cryptocurrency market data. 

The pipeline automatically triggers daily, fetches live market metrics (Price, Market Cap, 24h Volume) for top assets via a public API, transforms the unstructured JSON payloads into optimized relational tables, and appends them to a containerized data warehouse. This builds a robust, time-series historical dataset over time without manual intervention.

---

## 🏗️ System Architecture

The pipeline processes data through a structured 3-stage layer architecture:

1. **Extract:** A Python orchestration script executes a secure `GET` request targeting the CoinGecko API to retrieve real-time market data.
2. **Transform:** Raw nested JSON data is filtered, handled for network exceptions, timestamps are normalized to UTC, and structured into a clean tabular layout using Pandas.
3. **Load:** The structured dataset is safely appended to a local PostgreSQL data instance running inside an isolated Docker container environment.


---

## 🛠️ Tech Stack & Core Tools
* **Language:** Python 3.x (Requests, Pandas, SQLAlchemy)
* **Database Engine:** PostgreSQL
* **Containerization:** Docker & Docker Compose
* **Automation Scheduler:** Windows Task Scheduler / Linux Crontab (Local Deployment)
* **Database Client:** DBeaver

---

## 🗄️ Data Model & Schema Design

The target relational database utilizes a clean, time-series schema structured to support quick analytical queries:

```sql
CREATE TABLE crypto_prices (
    fetched_at TIMESTAMP WITHOUT TIME ZONE,
    coin_name VARCHAR(50),
    symbol VARCHAR(10),
    price_usd NUMERIC(18, 4),
    market_cap BIGINT,
    volume_24h BIGINT
);