from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, Auction, Bid
import datetime

# This line creates the tables in auction.db if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CREATE AN AUCTION ---
@app.post("/auctions")
def create_auction(title: str, starting_price: float, duration_minutes: int, db: Session = Depends(get_db)):
    auction = Auction(
        title=title,
        starting_price=starting_price,
        ends_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=duration_minutes)
    )
    db.add(auction)
    db.commit()
    db.refresh(auction)
    return auction

# --- PLACE A BID ---
@app.post("/auctions/{auction_id}/bids")
def place_bid(auction_id: int, bidder: str, amount: float, db: Session = Depends(get_db)):
    # Look up the auction
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    # Check if it's still active
    if datetime.datetime.utcnow() > auction.ends_at:
        raise HTTPException(status_code=400, detail="Auction has ended")

    # Get the current highest bid
    top_bid = db.query(Bid).filter(Bid.auction_id == auction_id).order_by(Bid.amount.desc()).first()
    min_bid = top_bid.amount if top_bid else auction.starting_price

    # Reject if bid isn't high enough
    if amount <= min_bid:
        raise HTTPException(status_code=400, detail=f"Bid must be higher than {min_bid}")

    # Save the bid
    bid = Bid(auction_id=auction_id, bidder=bidder, amount=amount)
    db.add(bid)
    db.commit()
    return {"message": "Bid placed", "amount": amount}

# --- GET AUCTION STATUS ---
@app.get("/auctions/{auction_id}")
def get_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")

    top_bid = db.query(Bid).filter(Bid.auction_id == auction_id).order_by(Bid.amount.desc()).first()

    return {
        "title": auction.title,
        "ends_at": auction.ends_at,
        "active": datetime.datetime.utcnow() < auction.ends_at,
        "current_highest_bid": top_bid.amount if top_bid else None,
        "leading_bidder": top_bid.bidder if top_bid else None,
    }