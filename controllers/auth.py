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
        if not "email" in data or not "password" in data or not "full name" in data:
            return jsonify({'error':'Required field is missing.'}),400
        else:
            full_name = data["full name"].strip()
            email = data["email"].strip()
            password = data["password"]
            val_result = check_valid.validate_register(full_name,email,password)
            if not val_result.status:
                return jsonify({'error':val_result.message}),400
            if self.auth_model.user_exists(email):
                return jsonify({'error':'user already registered. please login'}),400
            else:
                self.auth_model.user_register(full_name,email,password)
                token = access.encode_jwt_token(email,'not admin')
                return jsonify({'success':'You are successfully registered and loggged in as '+email,'authorization':token}),200

    def login(self,data,is_admin):
        if data is None:
            return jsonify({'error':'No Json Data received.'}),400
        if not "email" in data or not "password" in data:
            return jsonify({'error':'required field is missing. '}),400
        else:
            email = data["email"]
            password = data["password"]
            val_result = check_valid.validate_password(password)
            if not val_result.status:
                return jsonify({'error':val_result.message}),400
            if is_admin:
                val_result = check_valid.validate_admin_usename(email)
                if not val_result.status:
                    return jsonify({'error':val_result.message}),400
                if  self.auth_model.admin_login(email,password):
                    token = access.encode_jwt_token(email,'admin')
                    res = jsonify({'success':'You are loggged in as admin','authorization':token }),200
                    return res
                else:
                    return jsonify({'error':'incorrect username or password'}),400
            else:
                val_result = check_valid.validate_email(email)
                if not val_result.status:
                    return jsonify({'error':val_result.message}),400
                if not  self.auth_model.user_login(email,password):
                    return jsonify({'error':'invalid password or username'}),400
                else:
                    token = access.encode_jwt_token(email,'not admin')
                    return jsonify({'success':'You are loggged in as '+email,'authorization':token})
    def logout(self):
        access.blacklist_token(g.token,g.user)
        return jsonify({"success":"you are logged out"}),200
