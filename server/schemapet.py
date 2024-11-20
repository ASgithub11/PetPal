from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017"

# Initialize PyMongo
mongo = PyMongo(app)

@app.route('/api/pets', methods=['GET'])
def get_pets():
    pets_collection = mongo.db.pets  # Access the 'pets' collection
    pets = pets_collection.find()    # Retrieve all documents from the 'pets' collection
    pet_list = []
    for pet in pets:
        pet['_id'] = str(pet['_id'])  # Convert ObjectId to string for JSON serialization
        pet_list.append(pet)
    return jsonify(pet_list)

@app.route('/api/pets', methods=['POST'])
def add_pet():
    pet_data = request.get_json()
    pets_collection = mongo.db.pets  # Access the 'pets' collection
    result = pets_collection.insert_one(pet_data)  # Insert the new pet document
    return jsonify({"message": "Pet added successfully!", "pet_id": str(result.inserted_id)}), 201

@app.route('/api/pets/<pet_id>', methods=['GET'])
def get_pet(pet_id):
    pets_collection = mongo.db.pets
    pet = pets_collection.find_one({"_id": pet_id})
    if pet:
        pet['_id'] = str(pet['_id'])
        return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
