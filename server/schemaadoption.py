from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017"

# Initialize PyMongo
mongo = PyMongo(app)

# Define the Adoption Request Routes

@app.route('/api/adoption_requests', methods=['POST'])
def create_adoption_request():
    data = request.get_json()

    # Check if required fields are provided
    if 'user_id' not in data or 'pet_id' not in data:
        return jsonify({"error": "Missing required fields: user_id and pet_id"}), 400

    # Default status is 'pending'
    status = data.get('status', 'pending')
    message = data.get('message', '')

    # Prepare the adoption request document
    adoption_request = {
        "user_id": data['user_id'],  # User who is making the request
        "pet_id": data['pet_id'],    # Pet being adopted
        "status": status,            # Status of the request
        "message": message           # Optional message from user
    }

    # Insert the adoption request into the database
    result = mongo.db.adoption_requests.insert_one(adoption_request)

    return jsonify({"message": "Adoption request created", "adoption_request_id": str(result.inserted_id)}), 201

@app.route('/api/adoption_requests', methods=['GET'])
def get_adoption_requests():
    adoption_requests_collection = mongo.db.adoption_requests
    requests = adoption_requests_collection.find()

    adoption_request_list = []
    for request in requests:
        request['_id'] = str(request['_id'])  # Convert ObjectId to string for JSON serialization
        adoption_request_list.append(request)

    return jsonify(adoption_request_list)

@app.route('/api/adoption_requests/<adoption_request_id>', methods=['GET'])
def get_adoption_request(adoption_request_id):
    adoption_request = mongo.db.adoption_requests.find_one({"_id": ObjectId(adoption_request_id)})
    if adoption_request:
        adoption_request['_id'] = str(adoption_request['_id'])
        return jsonify(adoption_request)
    return jsonify({"error": "Adoption request not found"}), 404

@app.route('/api/adoption_requests/<adoption_request_id>', methods=['PUT'])
def update_adoption_request(adoption_request_id):
    data = request.get_json()
    status = data.get("status", None)
    message = data.get("message", None)

    # Only update status and/or message
    update_data = {}
    if status:
        update_data["status"] = status
    if message:
        update_data["message"] = message

    result = mongo.db.adoption_requests.update_one(
        {"_id": ObjectId(adoption_request_id)},
        {"$set": update_data}
    )

    if result.matched_count > 0:
        return jsonify({"message": "Adoption request updated successfully"}), 200
    else:
        return jsonify({"error": "Adoption request not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
