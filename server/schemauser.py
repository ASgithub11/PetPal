from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from hashlib import sha256  # Password hashing

# Initialize Flask app
app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017"

# Initialize PyMongo
mongo = PyMongo(app)

# Create indexes for username and email
mongo.db.users.create_index("username", unique=True)
mongo.db.users.create_index("email", unique=True)

# Function to hash a password
def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()

# Route to add a new user
@app.route('api/users', methods=['POST'])
def add_user():
    user_data = request.get_json()
    
    # Validate input (ensure all required fields are provided)
    if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data:
        return jsonify({"error": "Missing required fields: username, email, and password"}), 400
    
    # Hash the password before saving
    user_data['password'] = hash_password(user_data['password'])
    
    try:
        # Insert new user into MongoDB
        result = mongo.db.users.insert_one(user_data)
        return jsonify({"message": "User added successfully!", "user_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to retrieve all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users_collection = mongo.db.users  # Access the 'users' collection
    users = users_collection.find()    # Retrieve all documents from the 'users' collection
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        user_list.append(user)
    return jsonify(user_list)

# Route to retrieve a user by username
@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    users_collection = mongo.db.users
    user = users_collection.find_one({"username": username})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Route to verify user login (check username and password)
@app.route('/api/login', methods=['POST'])
def verify_login():
    login_data = request.get_json()
    
    # Ensure that username and password are provided
    if 'username' not in login_data or 'password' not in login_data:
        return jsonify({"error": "Missing required fields: username and password"}), 400

    username = login_data['username']
    password = login_data['password']

    # Hash the provided password to compare with stored hash
    hashed_password = hash_password(password)

    # Find the user by username
    user = mongo.db.users.find_one({"username": username})

    if user:
        if user['password'] == hashed_password:
            return jsonify({"message": "Login successful!"})
        else:
            return jsonify({"error": "Incorrect password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)

