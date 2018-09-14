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
    'username':username,
    'client id':get_unique_id()
    }

def get_session(client_id):
    if type(client_id) == type(None):
        return {}
    for userKey in Users.keys():
        if Users[userKey]['client id'] == client_id:
            return Users[userKey]
    return {}

def delete_session(client_id):
    if type(client_id) == type(None):
        return
    for userKey in Users.keys():
        if Users[userKey]['client id'] == client_id:
            del Users[userKey]

def get_admin_session():
    print adminSess.get_id()
    if adminSess.active :
        return adminSess.get_id()
    else:
        return None

def activate_admin_session():
    adminSess.activate()

def set_admin_session():
    adminSess = AdminSess()
    print adminSess.get_id()

def destroy_admin_sess():
    adminSess.destroy()

def get_unique_id():
    return uuid.uuid4().hex

def getClientId(username):
    return Users[username]['client id']


class AdminSess:
    def __init__(self):
        self.id = get_unique_id()
        self.active = False
    def get_id(self):
        return self.id
    def activate(self):
        self.active = True
    def destroy():
        self.active = False

adminSess = AdminSess()
