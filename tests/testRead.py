import unittest
from helper.functionRead import create_access_token

class TestCreateAccessToken(unittest.TestCase):
    def test_create_access_token(self):
        user_id = 1
        roles = 'user'
        token = create_access_token(identity={'id_user': user_id}, additional_claims={'roles': roles})
        
        self.assertIsNotNone(token, "Token should not be None")
        self.assertIn(f"token_for_{user_id}", token, "Token should contain user ID")
        self.assertIn(f"with_roles_{roles}", token, "Token should contain roles")

    def test_create_access_token_invalid(self):
        user_id = None  # ID tidak valid
        roles = 'user'
        token = create_access_token(identity={'id_user': user_id}, additional_claims={'roles': roles})
        
        self.assertIsNotNone(token, "Token should still be created for invalid user ID")
        self.assertIn(f"token_for_{user_id}", token, "Token should handle None user ID gracefully")
        self.assertIn(f"with_roles_{roles}", token, "Token should still include roles")

if __name__ == "__main__":
    unittest.main()
