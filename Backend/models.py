from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    exchange = Column(String)
    market_cap = Column(BigInteger)
    pe_ratio = Column(Numeric)
    dividend_yield = Column(Numeric)
    price = Column(Numeric)
    volume = Column(BigInteger)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("companies.symbol"), nullable=False)
    user_id = Column(String, default="default_user") 
    created_at = Column(TIMESTAMP, server_default=func.now())

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, ForeignKey("companies.symbol"), nullable=False)
    quantity = Column(Numeric, nullable=False)
    average_price = Column(Numeric, nullable=False)
    user_id = Column(String, default="default_user")
    created_at = Column(TIMESTAMP, server_default=func.now())
