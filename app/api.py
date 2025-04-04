from flask import Flask, request, jsonify
import os
from app.parser import Parser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'pptx'}
MAX_FILE_SIZE = 10 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File size exceeds the 10MB limit"}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        file.seek(0)

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file format. Only PDF and PPTX files are allowed"}), 400

        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length == 0:
            return jsonify({"error": "File is empty"}), 400

        if file_length > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({"error": "File size exceeds the 10MB limit"}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            return jsonify({"error": "A file with this name already exists"}), 400

        try:
            file.save(file_path)
        except IOError as e:
            return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

        parser = Parser(file_path)
        result = parser.parse_and_store()

        return jsonify({
            "message": "File uploaded and parsed successfully",
            "file_path": file_path,
            "database_result": result
        }), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/data', methods=['GET'])
def get_data():
    try:
        try:
            client = MongoClient(MONGODB_URI)
            client.server_info()
            print("Database connection successful")
        except Exception as db_error:
            print(f"DB Connection Error: {str(db_error)}")
            return jsonify({"error": "Database connection failed"}), 500

        db = client[MONGODB_DB]
        collection = db['pitch_deck_data']
        count = collection.count_documents({})

        data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB _id
        print(f"First document sample: {data[0] if data else 'No data'}")

        return jsonify(data), 200

    except Exception as e:
        print(f"Data fetch error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
