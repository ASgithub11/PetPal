import unittest
from datetime import datetime, timedelta
from authentication import generate_token, verify_token
import jwt

# test cases generated_token, verify_token, expired_token, and invalid_token from authentication.py

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.user_id = 123
        self.secret_key = "your_secret_key"
        self.token = generate_token(self.user_id)

    def test_generate_token(self):
        payload = jwt.decode(self.token, self.secret_key, algorithms=["HS256"])
        self.assertEqual(payload["user_id"], self.user_id)
        self.assertTrue("exp" in payload)

    def test_verify_token(self):
        user_id = verify_token(self.token)
        self.assertEqual(user_id, self.user_id)

    def test_expired_token(self):
        expired_token = jwt.encode({
            "user_id": self.user_id,
            "exp": datetime.utcnow() - timedelta(hours=1)
        }, self.secret_key, algorithm="HS256")
        user_id = verify_token(expired_token)
        self.assertIsNone(user_id)

    def test_invalid_token(self):
        invalid_token = self.token + "invalid"
        user_id = verify_token(invalid_token)
        self.assertIsNone(user_id)

if __name__ == "__main__":
    unittest.main()