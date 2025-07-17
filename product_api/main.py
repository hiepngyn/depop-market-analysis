from fastapi import FastAPI
from routes import listings

app = FastAPI()
app.include_router(listings.router)