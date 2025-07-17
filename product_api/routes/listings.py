from fastapi import APIRouter, Query
from db import collection
from typing import Optional
from bson import ObjectId

router = APIRouter()

def format_db(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/listings")
def get_lisitng(
    status: Optional[str] = Query(None),
    seller: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    limit: int = 10
):
    query = {}
    if status:
        query["status"] = status
    if seller:
        query["seller"] = seller
    if tag:
        query["tag"] = tag
    results = collection.find(query).limit(limit)
    return [format_db(doc) for doc in results]

