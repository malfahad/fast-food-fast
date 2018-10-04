from flask import jsonify,g,request
from models import auth
from utils.access import Access
from utils.validate import Validation


access = Access('my-secret-key')
check_valid = Validation()

class AuthController:
    def __init__(self,testing=False):
        self.auth_model = auth.AuthModel()
        pass

    def user_register(self,data):
        if data is None:
            return jsonify({'error':'No Json Data received. '}), 400

        if not "username" in data or not "password" in data or not "full name" in data:
            return jsonify({'error':'Required field is missing.'}),400
        else:
            full_name = data["full name"]
            username = data["username"]
            password = data["password"]

            if self.auth_model.user_exists(username):
                return jsonify({'error':'user already registered. please login'}),400
            else:
                self.auth_model.user_register(full_name,username,password)
                token = access.encode_jwt_token(username,'not admin')
                return jsonify({'success':'You are successfully registered and loggged in as '+username,'authorization':token}),200

    def login(self,data,is_admin):
        if data is None:
            return jsonify({'error':'No Json Data received.'}),400
        if not "username" in data or not "password" in data:
            return jsonify({'error':'required field is missing. '+str(data)}),206
        else:
            username = data["username"]
            password = data["password"]
            val_result = check_valid.validate_password(password)
            if not val_result.status:
                return jsonify({'error':val_result.message}),400

            if is_admin:
                val_result = check_valid.validate_admin_usename(username)
                if not val_result.status:
                    return jsonify({'error':val_result.message}),400
                if  self.auth_model.admin_login(username,password):
                    token = access.encode_jwt_token(username,'admin')
                    res = jsonify({'success':'You are loggged in as admin','authorization':token }),200
                    return res
                else:
                    return jsonify({'error':'incorrect username or password'}),400
            else:
                val_result = check_valid.validate_email(username)
                if not val_result.status:
                    return jsonify({'error':val_result.message}),400
                if not  self.auth_model.user_login(username,password):
                    return jsonify({'error':'invalid password or username'}),400
                else:
                    token = access.encode_jwt_token(username,'not admin')
                    return jsonify({'success':'You are loggged in as '+username,'authorization':token})
    def logout(self):
        access.blacklist_token(g.token,g.user)
        return jsonify({"success":"you are logged out"}),200
