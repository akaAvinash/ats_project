import unittest
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        """Test the sign-up functionality."""
        response = self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_login(self):
        """Test the login functionality."""
        self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('access_token', json_data)
        self.access_token = json_data['access_token'] 

    def test_protected(self):
        """Test accessing a protected route."""
        self.test_login()
        
        response = self.client.get('/protected', headers={
            'Authorization': f'Bearer {self.access_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are viewing a protected route!', response.data)

    def test_public_route(self):
        """Test a public route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, ATS!', response.data)

if __name__ == '__main__':
    unittest.main()
