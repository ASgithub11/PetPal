# this has been added to app.py

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/userDB"  # Change to your database URI

# Initialize PyMongo
mongo = PyMongo(app)

# Sample pet data to insert
sample_pets = [
    {
        "name": "Bella",
        "species": "Dog",
        "breed": "Labrador",
        "age": 4,
        "description": "A friendly and energetic dog who loves to play!",
        "is_available": True
    },
    {
        "name": "Max",
        "species": "Cat",
        "breed": "Siamese",
        "age": 2,
        "description": "A calm and affectionate cat, loves to nap.",
        "is_available": True
    },
    {
        "name": "Charlie",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "description": "Loyal, friendly, and great with kids!",
        "is_available": True
    },
    {
        "name": "Milo",
        "species": "Cat",
        "breed": "Persian",
        "age": 5,
        "description": "A bit shy but loves attention once comfortable.",
        "is_available": True
    },
    {
        "name": "Luna",
        "species": "Dog",
        "breed": "German Shepherd",
        "age": 6,
        "description": "Smart, alert, and a great watchdog.",
        "is_available": True
    },
    {
        "name": "Oliver",
        "species": "Cat",
        "breed": "Maine Coon",
        "age": 3,
        "description": "A large and affectionate cat, loves to play with string.",
        "is_available": False  # This one is not available for adoption
    }
]

# Insert sample pets into the MongoDB collection
@app.cli.command('seed_pets')
def seed_pets():
    pets_collection = mongo.db.pets
    for pet in sample_pets:
        pets_collection.insert_one(pet)
    print("Sample pets have been added to the database!")

if __name__ == "__main__":
    # Run the Flask app, only if the script is executed directly (not in CLI command)
    app.run(debug=True)
