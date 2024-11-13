from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory storage for users
users = []

# create new user
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400, description="Invalid request data")
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": request.json["name"],
        "email": request.json["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201