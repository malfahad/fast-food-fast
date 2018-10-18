import pytest
from app import app
import unittest
import json
from models import db
import config

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_home(self):
        """Check api home"""
        result = self.app.get('/api/v1')
        print result.data
        self.assertEqual('fast food fast api v1',result.data)

    def test_admin_login(self):
        self.endpoint = '/api/v1/auth/admin/login'
        """_with_valid_credentials"""
        result = self.app.post(self.endpoint, data = json.dumps({'email':'adminuser@gmail.com','password':'adminpass'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        """_with_wrong_email"""
        result = self.app.post(self.endpoint,data= json.dumps({'email':'not_the_admin@gmail.com','password':'adminpass'}),content_type='application/json')
        self.assertEqual(result.status_code,400)
        """_with_missing_field"""
        result = self.app.post(self.endpoint,data= json.dumps({'email':'adminuser@gmail.com'}),content_type='application/json')
        self.assertEqual(result.status_code,400)
    def test_admin_logout(self):
        self.endpoint = '/api/v1/auth/admin/logout'
        self.endpoint_login = '/api/v1/auth/admin/login'
        """ Test admin logout without access token"""
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,401)
        """ Test admin logout with access token"""
        result = self.app.post(self.endpoint_login, data = json.dumps({'email':'adminuser@gmail.com','password':'adminpass'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        access_token = result.json["authorization"]
        result = self.app.get(self.endpoint,headers={'Authorization':access_token})
        self.assertEqual(result.status_code,200)
        """ Test admin is actually logged out """
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,401)
