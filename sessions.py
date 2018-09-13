import uuid

class Session:
    def __init__(self):
        self.sessionId = uuid.uuid4().hex

ActiveSessions = []

Users = {}
admin = {'admin':'admin'}

def adminLogin(username,password):
    return username == 'admin' and password == admin[username]

def userLogin(username,password):
    if username in Users:
        return Users[username]['password'] == password
    else:
        return False

def userExists(username):
    return username in Users

def userRegister(full_name,username,password):
    Users[username] = {
    'password':password,
    'full name':full_name,
    'username':username
    }
