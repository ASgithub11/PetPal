from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
import re
from bson import ObjectId

app = Flask(__name__, static_folder='../client/dist', static_url_path='/')
# In-memory storage for users
users = []

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/userDB"

# Initialize PyMongo
mongo = PyMongo(app)

# Secret key for JWT (store securely in production)
SECRET_KEY = "your_secret_key"

# Define the 'users' collection
users_collection = mongo.db.users

# create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    print("Request data: ", request.json)
    if not request.json:
        abort(400, description="Invalid JSON")

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if not username or not email or not password:
        abort(400, description="Missing username, email, or password")

    hashed_password = bcrypt.hashpw(request.json["password"].encode('utf-8'), bcrypt.gensalt())
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "username": request.json["username"],
        "email": request.json["email"],
        "password": hashed_password
    }
    if users_collection.find_one({"username": username}):
        abort(400, description="Username already exists")
    if users_collection.find_one({"email": email}):
        abort(400, description="Email already exists")
    result = users_collection.insert_one(new_user)
    users.append(new_user)
    return jsonify({"message": "User created successfully", "user_id": str(result.inserted_id)}), 201

# login user
@app.route('/api/login', methods=['POST'])
def login_user():
    if not request.json:
        abort(400, description="Invalid JSON")

    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        abort(400, description="Missing username or password")
    user = users_collection.find_one({"username": username})

    if not user:
        abort(400, description="Incorrect login credentials")

    if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        abort(400, description="Incorrect login credentials")
    # Create a JWT token
    payload = {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Token expiration in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return jsonify({"message": "Login successful", "token": token}), 200

# function to verify a jwt token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# helper function for user lookup by id
def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)

# get specific user
def get_user(user_id):
    user = find_user(user_id)
    if user == None:
        abort(404, description="User not found")
    return jsonify(user)

# get all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = list(users_collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users), 200

# update user by id
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = find_user(user_id)
    if user == None:
        abort(404, description="User not found")
    if not request.json:
        abort(400, description="Invalid request data")
    
    user["name"] = request.json.get("name", user["name"])
    user["email"] = request.json.get("email", user["email"])
    return jsonify(user)


# delete user by id
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user(user_id)
    if user == None:
        abort(404, description="User not found")
    users.remove(user)
    return jsonify(user)

# this is a new section for the pets

# Define the 'pets' collection 
pets_collection = mongo.db.pets

# Define the route to get all pets
@app.route('/api/pets', methods=['GET'])
def get_pets():
    pets_collection = mongo.db.pets  # Access the 'pets' collection
    pets = pets_collection.find()    # Retrieve all documents from the 'pets' collection
    pet_list = []
    for pet in pets:
        pet['_id'] = str(pet['_id'])  # Convert ObjectId to string for JSON serialization
        pet_list.append(pet)
    return jsonify(pet_list)

# Define the route to add a pet
@app.route('/api/pets', methods=['POST'])
def add_pet():
    pet_data = request.get_json()
    pets_collection = mongo.db.pets  # Access the 'pets' collection
    result = pets_collection.insert_one(pet_data)  # Insert the new pet document
    return jsonify({"message": "Pet added successfully!", "pet_id": str(result.inserted_id)}), 201

# Define the route to get a specific pet
@app.route('/api/pets/<pet_id>', methods=['GET'])
def get_pet(pet_id):
    pets_collection = mongo.db.pets
    pet = pets_collection.find_one({"_id": pet_id})
    if pet:
        pet['_id'] = str(pet['_id'])
        return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404

# this section is for the favorites

# Define the 'favorite_pets' collection
favorite_pets_collection = mongo.db.favorite_pets

# Define the route to add a favorite pet
@app.route('/api/favorites', methods=['POST'])
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
    
# this section is for the adoption requests

# Define the 'adoption_requests' collection
adoption_requests_collection = mongo.db.adoption_requests

# Define the route to create an adoption request
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

# Define the route to get all adoption requests
@app.route('/api/adoption_requests', methods=['GET'])
def get_adoption_requests():
    adoption_requests_collection = mongo.db.adoption_requests
    requests = adoption_requests_collection.find()

    adoption_request_list = []
    for request in requests:
        request['_id'] = str(request['_id'])  # Convert ObjectId to string for JSON serialization
        adoption_request_list.append(request)

    return jsonify(adoption_request_list)

# Define the route to get a specific adoption request
@app.route('/api/adoption_requests/<adoption_request_id>', methods=['GET'])
def get_adoption_request(adoption_request_id):
    adoption_request = mongo.db.adoption_requests.find_one({"_id": ObjectId(adoption_request_id)})
    if adoption_request:
        adoption_request['_id'] = str(adoption_request['_id'])
        return jsonify(adoption_request)
    return jsonify({"error": "Adoption request not found"}), 404

# Define the route to update an adoption request
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
    
# define the route to delete an adoption request
@app.route('/api/adoption_requests/<adoption_request_id>', methods=['DELETE'])
def delete_adoption_request(adoption_request_id):
    result = mongo.db.adoption_requests.delete_one({"_id": ObjectId(adoption_request_id)})

    if result.deleted_count > 0:
        return jsonify({"message": "Adoption request deleted successfully"}), 200
    else:
        return jsonify({"error": "Adoption request not found"}), 404

# run the app
if __name__ == '__main__':
    app.run(debug=True)