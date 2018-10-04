import pytest
from app.app import app
import unittest
import json
from models import db
import config

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True
        #db.delete_test__tables()

    def test_api_home(self):
        """Check api home"""
        result = self.app.get('/api/v1')
        print result.data
        self.assertEqual('api in testing',result.data)

    def test_user_act_register(self):
        self.endpoint = "/api/v1/auth/register"
        """ Test user register with correct details """
        result = self.app.post(self.endpoint, data = json.dumps({'full name':'John Doe','username':'john.doe@gmail.com','password':'john.doe'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        """ Test user register when already exists """
        result = self.app.post(self.endpoint, data = json.dumps({'full name':'John Doe','username':'john.doe@gmail.com','password':'johndoe12'}),content_type='application/json')
        self.assertEqual(result.status_code,400)

    def test_user_login(self):
        self.endpoint = '/api/v1/auth/login'
        """_with_valid_credentials"""
        result = self.app.post(self.endpoint, data = json.dumps({'username':'john.doe@gmail.com','password':'john.doe'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        """_with_wrong_username"""
        result = self.app.post(self.endpoint,data= json.dumps({'username':'notthejohn.doe@gmail.com','password':'johndoe'}),content_type='application/json')
        print result.json
        self.assertEqual(result.status_code,400)

        """_with_missing_field"""
        result = self.app.post(self.endpoint,data= json.dumps({'username':'john.doe@gmail.com'}),content_type='application/json')
        self.assertEqual(result.status_code,206)
    def test_user_logout(self):
        self.endpoint = '/api/v1/auth/logout'
        self.endpoint_login = '/api/v1/auth/login'
        """ Test user logout without access token"""
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,401)
        """ Test user logout with access token"""
        result = self.app.post(self.endpoint_login, data = json.dumps({'username':'john.doe@gmail.com','password':'john.doe'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        access_token = result.json["authorization"]
        result = self.app.get(self.endpoint,headers={'Authorization':access_token})
        self.assertEqual(result.status_code,200)
        """ Test user is actually logged out """
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,401)
