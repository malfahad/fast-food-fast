from flask import Flask,request,Response,send_from_directory,render_template,jsonify,make_response,abort,g
from functools import wraps
from utils.access import Access
#from import sessions
#import orders
from controllers.auth import AuthController


app = Flask(__name__)
#Order = orders.Order
#MenuItem = orders.MenuItem
access = Access('my-secret-key')
auth = AuthController()

def ensure_admin_logged_in(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token = request.headers.get('Authorization')
        payload = access.decode_jwt_token(token)
        print 'admin' == payload.get('user')
        if not access.is_blacklisted(token) and payload.get('user_type') == 'admin':
            g.user = 'admin'
            g.token = token
            g.user_type = payload.get('user_type')
            return f(*args,**kwargs)
        else:
            abort(401)
    return decorated_function


def ensure_logged_in(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token = request.headers.get('Authorization')
        payload = access.decode_jwt_token(token)
        if not access.is_blacklisted(token) and not payload.get('user') == None:
            g.user = payload.get('user')
            g.token = token
            g.user_type = payload.get('user_type')
            return f(*args,**kwargs)
        else:
            abort(401)
    return decorated_function



def ensure_user_logged_in(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token = request.headers.get('Authorization')
        payload = access.decode_jwt_token(token)
        if not access.is_blacklisted(token) and not payload.get('user') == None and payload.get('user_type') == 'not admin':
            g.user = payload.get('user')
            g.token = token
            g.user_type = payload.get('user_type')
            return f(*args,**kwargs)
        else:
            abort(401)
    return decorated_function


# /api home
@app.route('/api/v1')
def home():
    print "app environemnt is "+str(app.config['ENV'])
    return 'fast food fast api v1'

#auth endpoints start here(

@app.route('/api/v1/auth/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    return auth.admin_login(data)

"""
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




#orders endpoints start here
@app.route('/api/v1/orders')
@ensure_logged_in
def get_orders():
    if g.user_type == 'admin':
        return jsonify(orders.get_orders())
    else:
        return jsonify(orders.get_orders_for(g.user))

@app.route('/api/v1/orders/<order_id>')
@ensure_logged_in
def get_order(order_id):
    order = orders.get_order_by_id(order_id)
    if not order is None:
        if g.user_type != 'admin' and order['ordered_by'] != g.user:
            abort(405);
        return jsonify({'status':'success','message':'Order Id is valid, list of all Orders attached',order_id:order}),200
    else:
        return jsonify({'status':'failed','message':'Order Id is invalid',order_id:None}),200

@app.route('/api/v1/orders', methods=['POST'])
@ensure_user_logged_in
def post_orders():
    if not "ordered_by" in request.form or not "total" in request.form or not "status" in request.form:
        return jsonify({'status':'error','message':'bad or corrupted data.'}),204
    else:
        ordered_by = request.form["ordered_by"]
        items = request.form["items"]
        total = request.form["total"]
        status = request.form["status"]
        order = Order(ordered_by)
        order.add_items(items)
        order.add_total(total)
        order.update_status(status)
        dbresult = order.save()
        if dbresult:
            return jsonify({'status':'success','message':'order added successfully'}),200
        else:
            return jsonify({'status':'error','message':'database error'}),400

@app.route('/api/v1/orders/<order_id>', methods=['PUT'])
@ensure_admin_logged_in
def put_order(order_id):
    if not "status" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    elif not orders.get_order_by_id(order_id) is None:
        return jsonify({'error':'unknown order Id.'})
    else:
        status = request.form["status"]
        orders_db.update_order_status(order_id,status)
        return jsonify({'success':'status updated to '+status}),200
#orders endpoints end here



#menu endpoints start here
@app.route('/api/v1/menu')
def get_menu():
    return jsonify(orders.get_menu()),200

@app.route('/api/v1/menu', methods=['POST'])
@ensure_admin_logged_in
def post_to_menu():
    if not "title" in request.form or not "desc" in request.form or not "amount" in request.form:
        return jsonify({'error':'bad or corrupted data.'}),200
    else:
        title = request.form["title"]
        desc = request.form["desc"]
        amount = request.form["amount"]
        if "img" in request.form:
            if len(request.form["img"]) > 5:
                img = request.form["img"]
            else:
                img = "http://placehold.it/200x200"
        else:
            img = "http://placehold.it/200x200"
        menu_item = MenuItem(title,desc,amount,img)
        dbresult = menu_item.save()
        if dbresult:
            return jsonify({'status':'success','message':'menu item  added successfully'}),200
        else:
            return jsonify({'status':'error','message':'database error'}),400

@app.route('/api/v1/menu/<id>', methods=['DELETE'])
@ensure_admin_logged_in
def remove_from_menu(id):
    if not orders.get_menu_item(id) is None:
        orders.remove_menu_item(id)
        return jsonify({'success':'menu item '+id+' deleted'}),200
    else:
        return jsonify({'error':'menu item '+id+' does not exist'}),200
#menu endpoints end here

"""
