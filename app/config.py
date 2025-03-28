import os

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB = os.environ.get("MONGODB_DB", "pitch_deck_data")
SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess-string"
# UPLOAD_FOLDER = 'uploads'
# MAX_CONTENT_LENGTH = 10 * 1024 * 1024
