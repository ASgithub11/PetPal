from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017"

# Initialize PyMongo
mongo = PyMongo(app)

# Define the route to add a favorite pet
@app.route('/api/favorite_pets', methods=['POST'])
def add_favorite_pet():
    data = request.get_json()

    # Check if required fields are provided
    if 'user_id' not in data or 'pet_id' not in data:
        return jsonify({"error": "Missing required fields: user_id and pet_id"}), 400

    # Create the favorite pet document
    favorite_pet = {
        "user_id": data['user_id'],  # User who marked the pet as favorite
        "pet_id": data['pet_id']     # Pet that was marked as favorite
    }

    # Insert the favorite pet into the database
    result = mongo.db.favorite_pets.insert_one(favorite_pet)

    return jsonify({"message": "Favorite pet added successfully!", "favorite_pet_id": str(result.inserted_id)}), 201

# Define the route to get all favorite pets for a specific user
@app.route('/api/favorite_pets/user/<int:user_id>', methods=['GET'])
def get_user_favorite_pets(user_id):
    # Query the database for all favorite pets of the user
    favorite_pets = mongo.db.favorite_pets.find({"user_id": user_id})

    # Convert the result to a list and prepare it for JSON response
    favorite_pet_list = []
    for pet in favorite_pets:
        pet['_id'] = str(pet['_id'])  # Convert ObjectId to string for JSON serialization
        favorite_pet_list.append(pet)

    return jsonify(favorite_pet_list)

# Define the route to remove a favorite pet
@app.route('/api/favorite_pets/<favorite_pet_id>', methods=['DELETE'])
def remove_favorite_pet(favorite_pet_id):
    # Delete the favorite pet by its ID
    result = mongo.db.favorite_pets.delete_one({"_id": ObjectId(favorite_pet_id)})

    if result.deleted_count > 0:
        return jsonify({"message": "Favorite pet removed successfully"}), 200
    else:
        return jsonify({"error": "Favorite pet not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
