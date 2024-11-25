from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
import re
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder='../client/dist', static_url_path='/', template_folder='../client/dist')
# In-memory storage for users
users = []

# MongoDB URI
app.config["MONGO_URI"] = os.environ.get("mongodb_uri")

# Initialize PyMongo
mongo = PyMongo(app)

# Secret key for JWT (store securely in production)
SECRET_KEY = "your_secret_key"

# Define the 'users' collection
users_collection = mongo.db.users

@app.route('/')
def index():
    return app.send_static_file('index.html')

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

# Sample pet data to insert
sample_pets = [
    {"name": "Bella", "species": "Dog", "breed": "Labrador", "age": 4, "description": "Friendly and energetic.", "is_available": True, "image_url": "https://muddling.me/wp-content/uploads/2023/12/long-life-copy.jpg"},
    {"name": "Max", "species": "Cat", "breed": "Siamese", "age": 2, "description": "Calm and affectionate.", "is_available": True, "image_url": "https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L2ZsMzU5MTkzNDU1MzItaW1hZ2Uta3BxazQwZmkuanBn.jpg"},
    {"name": "Charlie", "species": "Dog", "breed": "Golden Retriever", "age": 3, "description": "Loyal and friendly.", "is_available": True, "image_url": "https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3Vwd2s2MTc3NzU2Ni13aWtpbWVkaWEtaW1hZ2Uta293Ym8zYTkuanBn.jpg"}, 
    {"name": "Milo", "species": "Cat", "breed": "Persian", "age": 5, "description": "Shy, but loves attention.", "is_available": True, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0fMWsZxBTzQ0l0Wme9j3X-1qSLG-hUnbqVg&s"},
    {"name": "Luna", "species": "Dog", "breed": "German Shepherd", "age": 6, "description": "Smart and alert.", "is_available": True, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQE4V6Z8TsgP8XyReSeCrIkYB0PWDVkH3MXHg&s"},
    {"name": "Oliver", "species": "Cat", "breed": "Maine Coon", "age": 3, "description": "Affectionate and playful.", "is_available": False, "image_url" : "https://i2.pickpik.com/photos/410/926/471/maine-coon-cat-pet-relax-preview.jpg"}
]
# Flag to check if pets have already been seeded
pets_seeded = False

# Use before_request to seed pets if the flag is False
@app.before_request
def seed_pets():
    global pets_seeded
    if not pets_seeded:
        pets_collection = mongo.db.pets
        if pets_collection.count_documents({}) == 0:  # Only seed if the collection is empty
            for pet in sample_pets:
                pets_collection.insert_one(pet)
            print("Sample pets have been added to the database!")
            pets_seeded = True  # Set flag to True to prevent reseeding

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
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    try:
        favorite_pets_collection = mongo.db.favorite_pets
        favorite_pets_collection = favorite_pets_collection.find()

        favorite_pets_list = []
        for pet in favorite_pets_collection:
            pet['_id'] = str(pet['_id'])

        return jsonify(favorite_pets_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while retrieving favorite pets"}), 500


# Define the route to remove a favorite pet
from flask import request, jsonify
from bson import ObjectId

@app.route('/api/favorites/<favorite_pet_id>', methods=['DELETE'])
def remove_favorite_pet(favorite_pet_id):
    try:
        # Ensure the petId is valid ObjectId
        if not ObjectId.is_valid(favorite_pet_id):
            return jsonify({"error": "Invalid pet ID"}), 400
        
        # Delete the favorite pet by its ObjectId
        result = mongo.db.favorite_pets.delete_one({"_id": ObjectId(favorite_pet_id)})

        if result.deleted_count > 0:
            return jsonify({"message": "Favorite pet removed successfully"}), 200
        else:
            return jsonify({"error": "Favorite pet not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while removing the pet"}), 500


    
# this section is for the adoption requests

@app.route('/api/adopt', methods=['POST'])
def create_adoption_request():
    try:
        data = request.get_json()  # Get JSON data from the request
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        # Basic validation
        if not name or not email or not message:
            return jsonify({"error": "Please fill in all required fields"}), 400

        adoption_reqeusts_collection = mongo.db.adoption_requests
        adoption_request_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
        }
        result = adoption_reqeusts_collection.insert_one(adoption_request_data)  # Save to DB

         # Return a success response
        return jsonify({
            "message": "Adoption request created successfully",
            "request_id": str(result.inserted_id)  # Return the request ID in the response
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "There was an error. Please try again later."}), 500

# Define the route to get all adoption requests
@app.route('/api/adopt', methods=['GET'])
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