import db
users_db = db.UsersDB()
admins_db = db.AdminsDB()

def admin_login(username,password):
    result = admins_db.get_admin(username,password)
    return result != None and result != []

def user_login(username,password):
    result = users_db.get_user(username,password)
    return result != None and result != []

def user_exists(username):
    result = users_db.check_user(username)
    return result != None and result != []

def user_register(full_name,username,password):
    result = users_db.insert_user(full_name,username,password)
    return result
