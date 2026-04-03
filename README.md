# AI-Powered Stock Screener & Advisory Platform 🚀

An enterprise-grade, full-stack financial application that empowers investors to make data-driven stock market decisions using natural language queries and AI-powered insights.

## 📌 Project Overview
Instead of navigating complex financial tables or complicated syntax, users can type natural language questions like:
> *"Show me tech companies with high profit margins and a PE ratio under 30"*

The backend utilizes **Google Gemini (LLM)** to interpret the investor's intent, translates it into secure SQL, runs it against live Yahoo Finance data, and returns the actionable insights instantly to a high-end TradingView-styled interface.

---

## 🛠 Tech Stack

### Backend Architecture
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy ORM)
- **AI Integration:** Google Generative AI (`gemini-1.5-pro`)
- **Data Engineering:** `yfinance` for real-time ETL pipeline synchronization.

### Frontend Architecture
- **Structure:** Vanilla HTML5, CSS3, ES6 JavaScript
- **Design System:** Deep Slate Corporate Dark Theme (TradingView aesthetic)
- **Icons & Typography:** Google Material Symbols, Barlow/Inter fonts.

### DevOps
- Docker & Docker Compose

---

## 🚀 Key Features
*   **Natural Language Querying:** AI translates English into strict PostgreSQL queries dynamically.
*   **Live Market Synchronization:** Automatically scrapes the `yfinance` API to update core parameters (Market Cap, P/E, Margins) before execution to ensure data fidelity.
*   **Resiliency & Failover:** The AI agent falls back to secure mock-data parameters dynamically if rate-limited, ensuring the UI remains robust during investor presentations.
*   **Corporate UI:** A sleek, zero-dependency, ultra-fast frontend built native to the browser avoiding heavy React/Angular bundles.

---

## 💻 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- PostgreSQL (if running locally without Docker)
- A valid Google Gemini API Key.

### 2. Environment Variables
Create a `.env` file in the root directory (or export to your environment):
```bash
GEMINI_API_KEY="your-google-gemini-api-key"
DATABASE_URL="postgresql://postgres:password@localhost:5432/stock_screener"
```

### 3. Running with Docker (Recommended)
You can instantly spin up the entire full-stack platform using Docker:
```bash
docker-compose up -d --build
```
This automatically initializes the backend, seeds the live data using `yfinance`, and exposes the application to your localhost.

### 4. Running Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the FastAPI Server 
python Backend/main.py
```

### 5. Accessing the Application
Once the server is running, access the web interface at:
`http://127.0.0.1:8000/app/index.html`

---
*Built for the Infosys Internship Program*
