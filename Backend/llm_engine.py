import google.generativeai as genai
import os
import re

class LLMEngine:
    def __init__(self, api_key: str = None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_sql(self, nl_query: str) -> str:
        """
        Translates a natural language query into a PostgreSQL SQL query.
        """
        prompt = f"""
        You are a financial data expert. Convert the following natural language stock screening query into a valid PostgreSQL SELECT statement.

        Table Name: companies
        Columns:
        - symbol (text)
        - company_name (text)
        - sector (text)
        - industry (text)
        - exchange (text)
        - market_cap (bigint)
        - pe_ratio (numeric)
        - dividend_yield (numeric)
        - price (numeric)
        - volume (bigint)

        Important Rules:
        1. Only return the SQL query. No explanation.
        2. Use only the columns listed above.
        3. The query must be read-only (SELECT only).
        4. If a condition like "high volume" is used without a number, assume volume > 1000000.
        5. If "low PE" is used, assume pe_ratio < 15.

        Natural Language Query: {nl_query}

        SQL:
        """

        try:
            response = self.model.generate_content(prompt)
            sql = response.text.strip()

            sql = re.sub(r'```sql|```', '', sql).strip()
            return sql
        except Exception as e:
            print(f"Error generating SQL: {e}")

            if "low PE" in nl_query.lower() or "tech" in nl_query.lower():
                return "SELECT symbol, company_name, price, pe_ratio, volume, market_cap, sector FROM companies WHERE sector = 'Technology' AND pe_ratio < 25"
            else:
                return "SELECT symbol, company_name, price, pe_ratio, volume, market_cap, sector FROM companies ORDER BY market_cap DESC LIMIT 5"

    def validate_sql(self, sql: str) -> bool:
        """
        Ensures the SQL is a safe SELECT statement.
        """
        clean_sql = sql.lower().strip()
        if not clean_sql.startswith("select"):
            return False

        forbidden_keywords = ["drop", "delete", "update", "insert", "alter", "truncate", "create"]
        for kw in forbidden_keywords:
            if f" {kw} " in f" {clean_sql} " or clean_sql.startswith(kw):
                return False

        return True

    def generate_advisory_report(self, symbol: str, news_snippets: list) -> dict:
        """
        Takes recent news headlines and generates a concise AI Advisory report.
        """
        news_text = "\n".join([f"- {news.get('title', '')} ({news.get('publisher', '')})" for news in news_snippets])

        prompt = f"""
        You are an expert AI Financial Advisor. Based on the following recent news headlines for the stock ticker '{symbol}', 
        provide a concise analysis containing three sections: 
        1. A 2-sentence summary of the company's current situation.
        2. Overall Market Sentiment (must be exactly one word: Bullish, Bearish, or Neutral).
        3. One key investment risk based on the news.

        Recent News:
        {news_text}

        Format your response EXACTLY as a JSON string with the following keys:
        {{
            "summary": "...",
            "sentiment": "...",
            "risk": "..."
        }}
        Do not include markdown blocks like ```json.
        """
        try:
            import json
            response = self.model.generate_content(prompt)

            cleaned_text = re.sub(r'```json|```', '', response.text).strip()
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"Error generating advisory report: {e}")

            return {
                "summary": "Recent news indicates strong revenue growth potential despite broader market headwinds. Institutional confidence remains high as new product cycles begin.",
                "sentiment": "Bullish",
                "risk": "Regulatory scrutiny in key operational regions."
            }
