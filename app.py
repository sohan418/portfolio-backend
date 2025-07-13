from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Set up MongoDB client
client = MongoClient('mongodb+srv://sohanbisht418:054RQ21w0FftCzqz@cluster0.rrisa.mongodb.net/')  # Adjust the URI as needed
db = client['portfolio_db']  # Replace with your database name
collection = db['contact_messages']  # Replace with your collection name

@app.route('/submit', methods=['POST'])
def submit():
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

@app.route('/')
def hello():

    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)