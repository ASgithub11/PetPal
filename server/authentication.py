# this code has been rewritten in app.py

import jwt
from datetime import datetime, timedelta, timezone

# secret key for encoding and decoding JWT
SECRET_KEY = "your_secret_key"

# function to generate jwt token lasting 1 hour
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# function to verify a jwt token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
