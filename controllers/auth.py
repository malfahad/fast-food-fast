from flask import jsonify
from models import auth
from utils import access

class AuthController:
    def __init__(self):
        pass

    def admin_login(self,data):
        if not "username" in data or not "password" in data:
            return jsonify({'error':'bad or corrupted data. '+str(data)}),206
        else:
            username = data["username"]
            password = data["password"]
            if auth.admin_login(username,password):
                token = access.encode_jwt_token(username,'admin')
                res = jsonify({'success':'You are loggged in as admin','authorization':token }),200
                return res
            else:
                return jsonify({'error':'incorrect username or password'}),400


"""
@app.route('/api/v1/auth/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    print data

@app.route('/api/v1/auth/admin/logout')
@ensure_admin_logged_in
def get_admin_logout():
    access.blacklist_token(g.token,g.user)
    return jsonify({"success":"you are logged out"}),200



@app.route('/api/v1/auth/register', methods=['POST'])
def user_register():
    data = request.get_json()
    if not "username" in data or not "password" in data or not "full name" in data:
        return jsonify({'error':'bad or corrupted data.'}),400
    else:
        full_name = data["full name"]
        username = data["username"]
        password = data["password"]
        if sessions.user_exists(username):
            return jsonify({'error':'user already registered please login'}),400
        else:
            sessions.user_register(full_name,username,password)
            #user is registered
            token = access.encode_jwt_token(username,'not admin')
            res = make_response(jsonify({'success':'You are loggged in as '+username,'authorization':token})),200
            return res

@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    if not "username" in request.form or not "password" in request.form:
        return jsonify({'error':'bad or corrupted data.'}),200
    else:
        username = request.form["username"]
        password = request.form["password"]
        if not sessions.user_login(username,password):
            return jsonify({'error':'invalid password or username'}),200
        else:
            #user is logged in
            token = access.encode_jwt_token(username,'not admin')
            res = make_response(jsonify({'success':'You are loggged in as '+username,'authorization':token}))
            return res

@app.route('/api/v1/auth/logout')
@ensure_user_logged_in
def get_logout():
    access.blacklist_token(g.token,g.user)
    return jsonify({"success":"you are logged out"}),200
#auth endpoints end here

"""
