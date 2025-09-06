from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Get Mongo URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Missing MONGO_URI environment variable.")

# Set up MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client['portfolio_db']
    collection = db['contact_messages']
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

@app.route('/submit', methods=['POST'])
def submit():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON!"}), 400

    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, subject, message]):
        return jsonify({"error": "All fields are required!"}), 400

    try:
        collection.insert_one({
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        })
        return jsonify({"message": "Data stored successfully!"}), 201

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


@app.route('/')
def hello():
    return "Hello, World! The backend is running."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

