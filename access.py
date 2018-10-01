import jwt
import datetime
import json

class Access:
    def __init__(self,secret_key):
        self.secret_key = secret_key
        self.load_blacklist()

    def encode_jwt_token(self,user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'user': user_id
            }
            return jwt.encode(payload,self.secret_key,algorithm='HS256')
        except Exception as e:
             return e

    def decode_jwt_token(self,auth_header):
        try:
            return jwt.decode(auth_header,self.secret_key,algorithm = 'HS256')
        except:
            return {}

    def blacklist_token(self,token,user):
        self.blacklist[token]=user
        self.save_blacklist()

    def save_blacklist(self):
        with open('blacklist.json','w') as output:
            json.dump(self.blacklist,output)

    def is_blacklisted(self,token):
        return token in self.blacklist

    def load_blacklist(self):
        try:
            with open('blacklist.json','r') as input:
                self.blacklist = json.load(input)
        except:
            self.blacklist = {}
