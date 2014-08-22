from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref



Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    last_trade_price = Column(String)
    change = Column(String)
    
    def __init__(self, symbol):
        self.symbol = symbol