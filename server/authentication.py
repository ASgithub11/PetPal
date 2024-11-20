import jwt
from datetime import datetime, timedelta

# secret key for encoding and decoding JWT
SECRET_KEY = "my_secret_key"

# function to generate jwt token lasting 1 hour
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

