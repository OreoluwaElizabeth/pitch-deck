from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import MONGODB_URI, MONGODB_DB

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]

class PitchDeckData:
    def __init__(self, slide_title, text_content, metadata=None):
        self.slide_title = slide_title
        self.text_content = text_content
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "slide_title": self.slide_title,
            "text_content": self.text_content,
            "metadata": self.metadata
        }

    @staticmethod
    def insert_data(data):
        try:
            client = MongoClient(MONGODB_URI)
            db = client[MONGODB_DB]
            return db.pitch_deck_data.insert_one(data)
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    @staticmethod
    def get_all_data():
        try:
            client = MongoClient(MONGODB_URI)
            db = client[MONGODB_DB]
            return list(db.pitch_deck_data.find())
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            return []
