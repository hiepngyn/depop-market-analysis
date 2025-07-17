
import os 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('DATABASE_URL'))
db = client["products"]
collection = db["listing_info"]   
