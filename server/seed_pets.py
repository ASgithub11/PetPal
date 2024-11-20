from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')

# Select your database and collection
db = client['pet_adoption']
pets_collection = db['pets'] 

# Define the seed data for pets
pets = [
    {
        "id": 1,
        "name": "Bella",
        "species": "Dog",
        "breed": "Labrador",
        "age": 3,
        "description": "Friendly and energetic dog who loves to play.",
        "is_available": True
    },
    {
        "id": 2,
        "name": "Max",
        "species": "Cat",
        "breed": "Siamese",
        "age": 2,
        "description": "Quiet and loving cat, enjoys sitting by the window.",
        "is_available": True
    },
    {
        "id": 3,
        "name": "Charlie",
        "species": "Dog",
        "breed": "Beagle",
        "age": 4,
        "description": "Loyal and playful, great with kids.",
        "is_available": False  # This pet is not available
    },
    {
        "id": 4,
        "name": "Luna",
        "species": "Rabbit",
        "breed": "Holland Lop",
        "age": 1,
        "description": "Cute and fluffy bunny, loves fresh vegetables.",
        "is_available": True
    },
    {
        "id": 5,
        "name": "Oliver",
        "species": "Cat",
        "breed": "Maine Coon",
        "age": 5,
        "description": "Curious and friendly cat with a big personality.",
        "is_available": True
    }
]

# Insert the seed data into the collection
result = pets_collection.insert_many(pets)

# Print the inserted IDs
print(f"Inserted {len(result.inserted_ids)} pets.")
