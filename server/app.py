from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
import re

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

# run the app
if __name__ == '__main__':
    app.run(debug=True)