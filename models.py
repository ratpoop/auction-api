from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
import datetime

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    starting_price = Column(Float)
    ends_at = Column(DateTime)

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"))  # links to an auction
    bidder = Column(String)
    amount = Column(Float)
    placed_at = Column(DateTime, default=datetime.datetime.utcnow)