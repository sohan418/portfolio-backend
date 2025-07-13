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
    db = client['portfolio_db']  # Replace with your database name
    collection = db['contact_messages']  # Replace with your collection name
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get the form data from the request
        data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "message": request.form.get('message')
        }

        # Check if any required fields are missing
        if not all([data['name'], data['email'], data['message']]):
            return jsonify({"error": "All fields are required!"}), 400

        # Insert the data into MongoDB
        collection.insert_one(data)

        return jsonify({"message": "Data stored successfully!"}), 201
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
