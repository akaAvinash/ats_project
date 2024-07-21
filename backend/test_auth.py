import unittest
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        response = self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_login(self):
        self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        print("Login response data:", response.data)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('access_token', json_data)
        access_token = json_data['access_token']
        self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })

    def test_protected(self):
        self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        print("Login response data:", response.data)
        
        json_data = response.get_json()
        
        self.assertIn('access_token', json_data, "No access token received from login response")
        
        access_token = json_data['access_token']
        
        response = self.client.get('/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are viewing a protected route!', response.data)

if __name__ == '__main__':
    unittest.main()
