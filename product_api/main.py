from fastapi import FastAPI
from routes import listings, new

app = FastAPI()
app.include_router(listings.router)
app.include_router(new.router)