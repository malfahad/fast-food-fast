import db


class AuthModel:
    def __init__(self):
        self.users_db = db.UsersDB()
        self.admins_db = db.AdminsDB()
        pass
    def admin_login(self,username,password):
        result = self.admins_db.get_admin(username,password)
        return result != None and result != []

    def user_login(self,username,password):
        result = self.users_db.get_user(username,password)
        return result != None and result != []

    def user_exists(self,username):
        result = self.users_db.check_user(username)
        return result != None and result != []

    def user_register(self,full_name,username,password):
        result = self.users_db.insert_user(full_name,username,password)
        return result
