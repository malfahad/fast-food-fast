from flask import Flask,request,Response,send_from_directory,render_template,jsonify,make_response,abort,g
from utils.access import Access
from utils.decorated_functions import *
from controllers import AuthController,MenuController,OrdersController

app = Flask(__name__)
access = Access('my-secret-key')
auth_controller = AuthController()
menu_controller = MenuController()
orders_controller = OrdersController()

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

# /api home
@app.route('/api/v1')
def home():
    print "app environemnt is "+str(app.config['ENV'])
    return 'fast food fast api v1'

#auth endpoints start here
@app.route('/api/v1/auth/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    return auth_controller.login(data,True)

@app.route('/api/v1/auth/admin/logout')
@ensure_logged_in
def get_admin_logout():
    if g.user_type != 'admin':
        abort(401)#to be replaced with a proper error handler
    return auth_controller.logout()

@app.route('/api/v1/auth/register', methods=['POST'])
def user_register():
    data = request.get_json()
    return auth_controller.user_register(data)


@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    data = request.get_json()
    return auth_controller.login(data,False)

@app.route('/api/v1/auth/logout')
@ensure_logged_in
def get_logout():
    if g.user_type == 'admin':
        abort(401)#to be replaced with a proper error handler
    return auth_controller.logout()

#auth endpoints end here


#menu endpoints start here
@app.route('/api/v1/menu')
def get_menu():
    return menu_controller.get_menu()

@app.route('/api/v1/menu', methods=['POST'])
@ensure_logged_in
def post_to_menu():
    if g.user_type != 'admin':
        abort(401)#to be replaced with a proper error handler
    data = request.get_json()
    return menu_controller.post_to_menu(data)

@app.route('/api/v1/menu/<id>', methods=['DELETE'])
@ensure_logged_in
def remove_from_menu(id):
    if g.user_type != 'admin':
        abort(401)#to be replaced with a proper error handler
    return menu_controller.delete_menu_item(id)

#menu endpoints end here


#orders endpoints start here
@app.route('/api/v1/orders')
@ensure_logged_in
def get_orders():
    return orders_controller.get_orders()

@app.route('/api/v1/orders/<order_id>')
@ensure_logged_in
def get_order(order_id):
    return orders_controller.get_single_order(order_id)

@app.route('/api/v1/orders', methods=['POST'])
@ensure_logged_in
def post_orders():
    data = request.get_json()
    return orders_controller.add_new_order(data)

@app.route('/api/v1/orders/<order_id>', methods=['PUT'])
@ensure_logged_in
def put_order(order_id):
    if g.user_type != 'admin':
        abort(401)#to be replaced with a proper error handler
    data = request.json()
    return orders_controller.update_order_status(data)
#orders endpoints end here
