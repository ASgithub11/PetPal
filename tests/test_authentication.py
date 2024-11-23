import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from server.authentication import generate_token, verify_token
import jwt

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.user_id = 123
        self.secret_key = "your_secret_key"
        self.token = generate_token(self.user_id)
        print(f"Setup: Generated Token: {self.token}")

    def test_generate_token(self):
        print(f"Test Generate Token: Token: {self.token}")
        payload = jwt.decode(self.token, self.secret_key, algorithms=["HS256"])
        print(f"Test Generate Token: Payload: {payload}")
        self.assertEqual(payload["user_id"], self.user_id)
        self.assertTrue("exp" in payload)

    def test_verify_token(self):
        user_id = verify_token(self.token)
        print(f"Test Verify Token: Verified User ID: {user_id}")
        self.assertEqual(user_id, self.user_id)

    def test_expired_token(self):
        expired_token = jwt.encode({
            "user_id": self.user_id,
            "exp": datetime.utcnow() - timedelta(hours=1)
        }, self.secret_key, algorithm="HS256")
        print(f"Test Expired Token: Expired Token: {expired_token}")
        user_id = verify_token(expired_token)
        print(f"Test Expired Token: Verified User ID: {user_id}")
        self.assertIsNone(user_id)

    def test_invalid_token(self):
        invalid_token = self.token + "invalid"
        print(f"Test Invalid Token: Invalid Token: {invalid_token}")
        user_id = verify_token(invalid_token)
        print(f"Test Invalid Token: Verified User ID: {user_id}")
        self.assertIsNone(user_id)

if __name__ == "__main__":
    unittest.main()