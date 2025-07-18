from fastapi import APIRouter, HTTPException
from db import collection
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Pydantic model for new listing
class NewListing(BaseModel):
    title: str
    price: float
    currency: str
    seller: str
    url: str
    status: str = "available"
    tags: List[str] = []

def format_db(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("/new")
def create_listing(listing: NewListing):
    try:
        listing_data = listing.dict()
        listing_data["created_at"] = datetime.utcnow().isoformat() + "Z"
        
        result = collection.insert_one(listing_data)
        
        created_listing = collection.find_one({"_id": result.inserted_id})
        return format_db(created_listing)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create listing: {str(e)}")
