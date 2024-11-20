from flask import Flask, request, jsonify, abort

app = Flask(__name__)
# In-memory storage for users
users = []

# create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    print("Request data: ", request.json)
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400, description="Invalid request data")
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": request.json["name"],
        "email": request.json["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

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
    return jsonify(users)

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

# run the app
if __name__ == '__main__':
    app.run(debug=True)