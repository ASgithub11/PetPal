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
        "is_available": True,
        "image_url": "https://muddling.me/wp-content/uploads/2023/12/long-life-copy.jpg"
    },
    {
        "name": "Max",
        "species": "Cat",
        "breed": "Siamese",
        "age": 2,
        "description": "A calm and affectionate cat, loves to nap.",
        "is_available": True,
    },
    {
        "name": "Charlie",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "description": "Loyal, friendly, and great with kids!",
        "is_available": True,
    },
    {
        "name": "Milo",
        "species": "Cat",
        "breed": "Persian",
        "age": 5,
        "description": "A bit shy but loves attention once comfortable.",
        "is_available": True,
    },
    {
        "name": "Luna",
        "species": "Dog",
        "breed": "German Shepherd",
        "age": 6,
        "description": "Smart, alert, and a great watchdog.",
        "is_available": True,
    },
    {
        "name": "Oliver",
        "species": "Cat",
        "breed": "Maine Coon",
        "age": 3,
        "description": "A large and affectionate cat, loves to play with string.",
        "is_available": True,
    },
    {
        "name": "Rocky",
        "species": "Dog",
        "breed": "Bulldog",
        "age": 4,
        "description": "A tough exterior but a sweetheart at heart, loves belly rubs.",
        "is_available": True,
        "image_url": "https://cdn12.picryl.com/photo/2016/12/31/dog-summer-bulldog-animals-7bd543-1024.jpg"
    },
    {
        "name": "Salem",
        "species": "Cat",
        "breed": "Black Cat",
        "age": 3,
        "description": "Mysterious and independent, but enjoys quiet time with humans.",
        "is_available": True,
        "image_url": "https://www.publicdomainpictures.net/pictures/240000/nahled/black-cat-1508769961FHr.jpg"
    },
    {
        "name": "Ruby",
        "species": "Dog",
        "breed": "Dachshund",
        "age": 2,
        "description": "Tiny but mighty, loves to burrow into blankets.",
        "is_available": True,
        "image_url": "https://media.istockphoto.com/id/839279536/photo/a-miniature-dachshund-standing-in-long-grass.jpg?s=612x612&w=0&k=20&c=1ChA2Nk4M9TYjxmyefmEeMXwzzdBkMUD2PL5Rez9Vjk="
    },
    {
        "name": "Chester",
        "species": "Cat",
        "breed": "British Shorthair",
        "age": 4,
        "description": "Chubby and playful, loves to chase laser pointers.",
        "is_available": True,
        "image_url": "https://media.istockphoto.com/id/1319774380/photo/british-cat-lying-cat-tree-scratching-post.jpg?s=612x612&w=0&k=20&c=xHChZkY0pRw5-ZMdT_qulNxWS1sWP_OUXUihYg3cZjo="
    },
    {
        "name": "Zara",
        "species": "Dog",
        "breed": "Poodle",
        "age": 5,
        "description": "Elegant and friendly, loves to be pampered and brushed.",
        "is_available": True,
        "image_url": "https://images.stockcake.com/public/4/9/4/494b8641-1ec7-464f-880e-12440232abb7_large/elegant-poodle-posing-stockcake.jpg"
    },
    {
        "name": "Cleo",
        "species": "Cat",
        "breed": "Egyptian Mau",
        "age": 2,
        "description": "Active and curious, loves to explore and climb high places.",
        "is_available": True,
        "image_url": "https://images.rawpixel.com/image_social_landscape/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcHg5MzIxNTgtaW1hZ2Uta3d5bzF2YXQuanBn.jpg"
    },
    {
        "name": "Bailey",
        "species": "Dog",
        "breed": "Beagle",
        "age": 3,
        "description": "Friendly, curious, and loves to go on long walks.",
        "is_available": True,
        "image_url": "https://cdn2.picryl.com/photo/2008/05/18/beaglehappy2-1fe81c-1024.jpg"
    },
    {
        "name": "Simba",
        "species": "Cat",
        "breed": "Ragdoll",
        "age": 1,
        "description": "Gentle, affectionate, and loves to follow you around the house.",
        "is_available": True,
        "image_url": "https://www.publicdomainpictures.net/pictures/90000/nahled/gorgeous-ragdoll-cat.jpg"
    },
    {
        "name": "Toby",
        "species": "Dog",
        "breed": "Cocker Spaniel",
        "age": 2,
        "description": "Playful, loving, and enjoys cuddles after a long walk.",
        "is_available": True,
        "image_url": "https://cdn12.picryl.com/photo/2016/12/31/dog-cocker-pet-animals-a5611b-1024.jpg"
    },
    {
        "name": "Jasper",
        "species": "Cat",
        "breed": "Abyssinian",
        "age": 4,
        "description": "Energetic, agile, and loves interactive play sessions.",
        "is_available": True,
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwPHFshmH3o_-U3Os6Ozyy0wKRuC-EnL5PEw&s"
    },
    {
        "name": "Maggie",
        "species": "Dog",
        "breed": "Boxer",
        "age": 6,
        "description": "Energetic and playful, loves to play fetch and run in the yard.",
        "is_available": True,
        "image_url": "https://lh5.googleusercontent.com/proxy/iQTnsXZ0Hm9uie2jI_t79S6gNXUVmWFfzP2ZcIu9gnQhsNjZIDgbS_r9zHAzWr07fA_DPh8yaqHf6ab-DDv03tfO1SZFC2aQBtf7bYAvuuMl8XQ"
    },
    {
        "name": "Nala",
        "species": "Cat",
        "breed": "Bengal",
        "age": 3,
        "description": "Active and playful, loves climbing and being the center of attention.",
        "is_available": True,
        "image_url": "https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcHgxNDA3MTE2LWltYWdlLWt3dnh6NXNzLWt6aHZ1ZnhoLmpwZw.jpg"
    },
    {
        "name": "Daisy",
        "species": "Dog",
        "breed": "Shih Tzu",
        "age": 4,
        "description": "Sweet, loyal, and loves snuggling on the couch.",
        "is_available": True,
        "image_url": "https://cdn12.picryl.com/photo/2016/12/31/dog-shih-tzu-puppy-animals-23c668-640.jpg"
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
