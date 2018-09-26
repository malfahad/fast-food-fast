import uuid

class Session:
    def __init__(self):
        self.session_id = uuid.uuid4().hex

active_sessions = []

users = {}
admin = {'admin':'admin'}

def admin_login(username,password):
    return username == 'admin' and password == admin[username]

def user_login(username,password):
    if username in users:
        return users[username]['password'] == password
    else:
        return False

def user_exists(username):
    return username in users

def user_register(full_name,username,password):
    users[username] = {
    'password':password,
    'full name':full_name,
    'username':username,
    'client id':get_unique_id()
    }

def get_session(client_id):
    if type(client_id) == type(None):
        return {}
    for user_key in users.keys():
        if users[user_key]['client id'] == client_id:
            return users[userKey]
    return {}

def delete_session(client_id):
    if type(client_id) == type(None):
        return
    for user_key in users.keys():
        if users[user_key]['client id'] == client_id:
            del users[userKey]

def get_admin_session():
    print admin_sess.get_id()
    if admin_sess.active :
        return admin_sess.get_id()
    else:
        return None

def activate_admin_session():
    admin_sess.activate()

def set_admin_session():
    admin_sess = AdminSess()
    print admin_sess.get_id()

def destroy_admin_sess():
    admin_sess.destroy()

def get_unique_id():
    return uuid.uuid4().hex

def getClientId(username):
    return users[username]['client id']


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

admin_sess = AdminSess()
