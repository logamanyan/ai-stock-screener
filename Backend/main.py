from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import yfinance as yf

from database import get_db
from models import Company, Watchlist, Portfolio
from llm_engine import LLMEngine
from pydantic import BaseModel
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import google.generativeai as genai

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Critical: No GEMINI_API_KEY found in environment variables. Do not hardcode credentials.")
llm = LLMEngine(api_key=api_key)

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Frontend")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="static")

class QueryRequest(BaseModel):
    raw_query: str

class ScreenerResponse(BaseModel):
    status: str
    total_matches: int
    stocks: list
    generated_sql: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    return {"db": "connected"}

@app.get("/metadata/stocks")
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Company).all()

    return [
        {
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "sector": stock.sector,
            "market_cap": stock.market_cap
        }
        for stock in stocks
    ]

@app.post("/api/v1/screener/execute", response_model=ScreenerResponse)
def execute_screener(request: QueryRequest, db: Session = Depends(get_db)):
    raw_query = request.raw_query

    sql = llm.generate_sql(raw_query)

    if not sql or not llm.validate_sql(sql):
        return {
            "status": "error",
            "total_matches": 0,
            "stocks": [],
            "message": "Failed to generate valid SQL"
        }

    try:
        result = db.execute(text(sql))
        stocks = [dict(row._mapping) for row in result]

        return {
            "status": "success",
            "total_matches": len(stocks),
            "stocks": stocks,
            "generated_sql": sql
        }
    except Exception as e:
        return {
            "status": "error",
            "total_matches": 0,
            "stocks": [],
            "message": f"SQL Execution Error: {str(e)}"
        }

@app.get("/api/v1/live-price/{symbol}")
def get_live_price(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.info
        return {
            "symbol": symbol,
            "current_price": data.get("currentPrice") or data.get("regularMarketPrice"),
            "change": data.get("regularMarketChange"),
            "percent_change": data.get("regularMarketChangePercent")
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v1/advisor/{symbol}")
def get_ai_advisor_report(symbol: str):
    try:
        ticker = yf.Ticker(symbol)

        news = ticker.news[:5] if ticker.news else []

        if not news:
            return {
                "status": "error",
                "message": "No recent news found for this symbol."
            }

        report = llm.generate_advisory_report(symbol, news)
        return {
            "status": "success",
            "symbol": symbol,
            "data": report
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate report: {str(e)}"}

class WatchlistAdd(BaseModel):
    symbol: str

@app.get("/api/v1/watchlist")
def get_watchlist(db: Session = Depends(get_db)):
    items = db.query(Watchlist).filter(Watchlist.user_id == "default_user").all()
    return {"status": "success", "data": [item.symbol for item in items]}

@app.post("/api/v1/watchlist")
def add_to_watchlist(request: WatchlistAdd, db: Session = Depends(get_db)):
    item = Watchlist(symbol=request.symbol, user_id="default_user")
    db.add(item)
    db.commit()
    return {"status": "success", "message": f"{request.symbol} added to watchlist"}

@app.delete("/api/v1/watchlist/{symbol}")
def remove_from_watchlist(symbol: str, db: Session = Depends(get_db)):
    db.query(Watchlist).filter(Watchlist.symbol == symbol, Watchlist.user_id == "default_user").delete()
    db.commit()
    return {"status": "success", "message": "Removed from watchlist"}

class PortfolioAdd(BaseModel):
    symbol: str
    quantity: float
    average_price: float

@app.get("/api/v1/portfolio")
def get_portfolio(db: Session = Depends(get_db)):
    items = db.query(Portfolio).filter(Portfolio.user_id == "default_user").all()

    results = []
    total_portfolio_value = 0
    total_portfolio_investment = 0

    for item in items:
        company = db.query(Company).filter(Company.symbol == item.symbol).first()
        live_price = float(company.price) if company and company.price else float(item.average_price)

        avg_price = float(item.average_price)
        qty = float(item.quantity)

        investment = qty * avg_price
        current_val = qty * live_price
        pl = current_val - investment
        pl_pct = (pl / investment * 100) if investment > 0 else 0

        total_portfolio_investment += investment
        total_portfolio_value += current_val

        results.append({
            "symbol": item.symbol,
            "quantity": qty,
            "average_price": avg_price,
            "live_price": live_price,
            "investment": investment,
            "current_val": current_val,
            "profit_loss": pl,
            "pl_percent": pl_pct
        })

    return {
        "status": "success", 
        "summary": {
            "total_investment": total_portfolio_investment,
            "current_value": total_portfolio_value,
            "total_pl": total_portfolio_value - total_portfolio_investment,
            "total_pl_percent": ((total_portfolio_value - total_portfolio_investment) / total_portfolio_investment * 100) if total_portfolio_investment > 0 else 0
        },
        "data": results
    }

@app.post("/api/v1/portfolio")
def add_to_portfolio(request: PortfolioAdd, db: Session = Depends(get_db)):
    item = Portfolio(symbol=request.symbol, quantity=request.quantity, average_price=request.average_price, user_id="default_user")
    db.add(item)
    db.commit()
    return {"status": "success", "message": "Added to portfolio"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
