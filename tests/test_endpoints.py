import pytest
import app
import unittest
import json
import db
import config

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        db.db_url = config.TEST_DB_URL

    def test_api_home(self):
        """Check api home"""
        result = self.app.get('/api/v1')
        print result.data
        self.assertEqual('fast food fast api v1',result.data)

    def test_admin_login(self):
        self.endpoint = '/api/v1/auth/admin/login'
        #_with_valid_credentioals
        result = self.app.post(self.endpoint, data = json.dumps({'username':'admin','password':'admin'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        #_with_wrong_username
        result = self.app.post(self.endpoint,data= json.dumps({'username':'not_the_admin','password':'admin'}),content_type='application/json')
        self.assertEqual(result.status_code,400)
        #_with_missing_field
        result = self.app.post(self.endpoint,data= json.dumps({'username':'admin'}),content_type='application/json')
        self.assertEqual(result.status_code,400)
    def test_admin_logout(self):
        self.endpoint = '/api/v1/auth/admin/logout'
        self.endpoint_login = '/api/v1/auth/admin/login'
        """ Test admin login without access token"""
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,405)
        """ Test admin login with access token"""
        result = self.app.post(self.endpoint_login, data = json.dumps({'username':'admin','password':'admin'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        access_token = result.json["authorization"]
        result = self.app.get(self.endpoint,headers={'Authorization':access_token})
        self.assertEqual(result.status_code,200)
        """ Test admin is actually logged out """
        result = self.app.get(self.endpoint)
        self.assertEqual(result.status_code,405)

    def test_user_register(self):
        self.endpoint = "/api/v1/auth/register"
        """ Test user register with correct details """
        result = self.app.post(self.endpoint, data = json.dumps({'full name':'John Doe','username':'johndoe@gmail.com','password':'johndoe'}),content_type='application/json')
        self.assertEqual(result.status_code,200)
        """ Test user register when already exists """
        result = self.app.post(self.endpoint, data = json.dumps({'full name':'John Doe','username':'johndoe@gmail.com','password':'johndoe'}),content_type='application/json')
        self.assertEqual(result.status_code,400)
