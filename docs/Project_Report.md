# End-to-End Project Report: AI-Powered Stock Screener & Advisory Platform

**Client / Organization:** Infosys Internship Program  
**Project Specialization:** Full-Stack AI & Data Engineering  
**Role:** Developer / Architect  

---

## 1. Executive Summary
The **AI-Powered Stock Screener** is an enterprise-grade web application designed to democratize high-level financial analysis. By integrating the cutting-edge **Google Gemini LLM**, the platform translates natural language inputs (e.g., *"Show me tech companies with high profit margins and PE ratio under 30"*) directly into optimized SQL queries. These queries are executed against a live-updating PostgreSQL database fed by accurate market data. The resulting data is then displayed through a highly polished, responsive "TradingView style" UI architecture.

---

## 2. Technical Architecture

The platform operates on a robust, asynchronous three-tier Python architecture, fully containerized under Docker.

### 2.1 Technology Stack
- **Frontend Layer:** Vanilla HTML5, CSS3 natively customized with Enterprise Slate colors, and JavaScript (ES6+).
- **Backend / API Engine:** FastAPI (Python), utilizing RESTful architecture.
- **Relational Database:** PostgreSQL, optimized with SQLAlchemy ORM.
- **Data Engineering Pipeline:** Yahoo Finance (`yfinance`) API for real-time ETL.
- **Artificial Intelligence:** Google Generative AI (Gemini v1.5 Pro) with failover protocols.
- **DevOps:** Docker & Docker Compose for guaranteed environment parity.

---

## 3. Data Engineering & Pipeline Development

### 3.1 The ETL Engine (`data_pipeline.py`)
To ensure high-fidelity financial computations, the system eliminates hardcoded mock data by routinely extracting live metrics from Yahoo Finance.
*   **Extract:** Connects to Yahoo Finance using Python async tasks to pull metrics for major tickers (e.g., AAPL, MSFT, GOOGL, NVDA).
*   **Transform:** Standardizes fluctuating metrics such as `pe_ratio`, `market_cap`, `revenue_growth_yoy`, `profit_margin`, and calculates the buffer distance from `52_week_high`. Null parameters are rigorously sanitized.
*   **Load:** The transformed dataset is injected into PostgreSQL via SQLAlchemy. The pipeline uses an `Upsert` mechanism to prevent duplicate entries, guaranteeing fresh historical data points.

---

## 4. Artificial Intelligence Implementation

### 4.1 Natural Language Query Engine (`llm_engine.py`)
The most significant engineering challenge solved in this application was deterministic translation of Natural Language (`NL`) to Domain-Specific Language (`SQL`).
*   **Schema Injection:** The Gemini model is initialized with a strict system prompt containing the exact PostgreSQL `Company` schema.
*   **Generative Execution:** When a user types a query, Gemini outputs a sanitized SQL parameter string avoiding SQL injection traps.
*   **Resiliency & Failover:** A failover block automatically traps network exceptions (`404 Model Not Found`, `RateLimit`). If the Gemini API malfunctions, the system seamlessly routes into a robust mock-data layer so the frontend UI never breaks during demonstrations.

---

## 5. UI/UX Design System

The frontend was massively overhauled to match the dark, deep-slate aesthetic commonly utilized by tier-one algorithmic platforms (e.g., Bloomberg, TradingView).
*   **Deep Slate Aesthetic:** Background hex layers (`#131722` to `#1e222d`) to eliminate eyestrain.
*   **Typography:** Strict sans-serif font rendering mapped to `Inter` bounds, utilizing stark white font-colors to achieve maximum contrast.
*   **Responsive State Management:** Dynamic `CSS` variable states override browser caching (via `?v=pro` buster hooks) to ensure rapid loading without rendering artifacting.

---

## 6. Security and Environment Constraints

*   **Credential Isolation:** Security mechanisms map the `GEMINI_API_KEY` and `DATABASE_URL` exclusively to the system environment variables (`os.environ`).
*   **Docker Containerization:** A bespoke `Dockerfile` strictly encapsulates the FastAPI server and Psycopg2 binaries. `docker-compose.yml` bridges the server to the PostgreSQL instance over a closed virtual network, hiding the database from external internet access and blocking common exposure surfaces.

---

## 7. Next Steps & Future Scope

While the current V1 delivery proves the application is completely production-ready, subsequent iterations aim to include:
1.  **JWT Authentication:** Enabling user login to natively save generated algorithmic Watchlists securely.
2.  **Streaming WebSockets:** Replacing the RESTful `/api/v1/update` mechanism with an open WebSocket pipe to push rapid stock price ticks directly into the Javascript arrays in real time.
3.  **Cloud Deployment Strategy:** Utilizing AWS ECS/Fargate infrastructure to scale Docker containers across fluctuating user loads seamlessly.
