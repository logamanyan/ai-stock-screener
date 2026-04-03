import yfinance as yf
from database import SessionLocal
from models import Company
from decimal import Decimal
import time

TARGET_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "KOTAKBANK.NS",
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"
]

def map_yf_to_company(symbol: str, info: dict) -> dict:
    """
    Transforms yfinance .info dictionary into our Company model schema.
    Handles missing keys gracefully.
    """
    pe_ratio = info.get("trailingPE") or info.get("forwardPE")
    dividend_yield = info.get("dividendYield") or info.get("trailingAnnualDividendYield")
    price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")

    return {
        "symbol": symbol,
        "company_name": info.get("shortName", info.get("longName", symbol)),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "exchange": info.get("exchange", "Unknown"),
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": Decimal(str(pe_ratio)) if pe_ratio else None,
        "dividend_yield": Decimal(str(dividend_yield)) if dividend_yield else None,
        "price": Decimal(str(price)) if price else None,
        "volume": info.get("volume", info.get("regularMarketVolume", 0))
    }

def run_pipeline():
    print(f"🚀 Starting data ingestion for {len(TARGET_SYMBOLS)} stocks...")
    db = SessionLocal()

    try:
        success_count = 0
        error_count = 0

        for symbol in TARGET_SYMBOLS:
            print(f"Fetching data for {symbol}...")
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info

                if not info or "symbol" not in info:
                    print(f"  ⚠️ Skipping {symbol} (No data found)")
                    error_count += 1
                    continue

                stock_data = map_yf_to_company(symbol, info)

                existing = db.query(Company).filter(Company.symbol == symbol).first()
                if existing:

                    for key, value in stock_data.items():
                        setattr(existing, key, value)
                    print(f"  🔄 Updated {symbol}")
                else:

                    new_company = Company(**stock_data)
                    db.add(new_company)
                    print(f"  ✅ Inserted {symbol}")

                success_count += 1

                time.sleep(0.5)

            except Exception as e:
                print(f"  ❌ Error fetching/processing {symbol}: {e}")
                error_count += 1

        db.commit()
        print(f"\n🎉 Pipeline Finished! Successfully processed: {success_count}. Errors: {error_count}.")

    except Exception as e:
        db.rollback()
        print(f"Critical Pipeline Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_pipeline()
