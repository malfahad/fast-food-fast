from flask import Flask,request,Response,send_from_directory,render_template,jsonify,make_response,abort,g
from functools import wraps
from access import Access
import sessions
import orders

app = Flask(__name__)
Order = orders.Order
MenuItem = orders.MenuItem
access = Access('my-secret-key')

def ensure_admin_logged_in(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token = request.headers.get('Authorization')
        print access.decode_jwt_token(token)
        print not access.is_blacklisted(token)
        print 'admin' == access.decode_jwt_token(token).get('user')
        if not access.is_blacklisted(token) and 'admin' == access.decode_jwt_token(token).get('user'):
            g.user = 'admin'
            g.token = token
            return f(*args,**kwargs)
        else:
            abort(405)
    return decorated_function


def ensure_user_logged_in(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        token = request.headers.get('Authorization')
        payload = access.decode_jwt_token(token)
        if not access.is_blacklisted(token) and not payload.get('user') == None:
            g.user = payload.get('user')
            g.token = token
            return f(*args,**kwargs)
        else:
            abort(405)
    return decorated_function


# /api home
@app.route('/api/v1')
def home():
    return 'fast food fast api v1'

#auth endpoints start here

@app.route('/api/v1/admin/login', methods=['POST'])
def admin_login():
    if not "username" in request.form or not "password" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    else:
        username = request.form["username"]
        password = request.form["password"]
        if sessions.admin_login(username,password):
            token = access.encode_jwt_token('admin')
            res = make_response(jsonify({'success':'You are loggged in as admin','authorization':token })),200
            return res
        else:
            return jsonify({'error':'incorrect username or password'}),200

@app.route('/api/v1/admin/logout')
@ensure_admin_logged_in
def get_admin_logout():
    access.blacklist_token(g.token,g.user)
    return jsonify({"success":"you are logged out"}),200



@app.route('/api/v1/register', methods=['POST'])
def user_register():
    if not "username" in request.form or not "password" in request.form or not "full name" in request.form:
        return jsonify({'error':'bad or corrupted data.'}),204
    else:
        full_name = request.form["full name"]
        username = request.form["username"]
        password = request.form["password"]
        if sessions.user_exists(username):
            return jsonify({'error':'user already registered please login'})
        else:
            sessions.user_register(full_name,username,password)
            #user is registered
            token = access.encode_jwt_token(username)
            res = make_response(jsonify({'success':'You are loggged in as '+username,'authorization':token}))
            return res

@app.route('/api/v1/login', methods=['POST'])
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
            token = access.encode_jwt_token(username)
            res = make_response(jsonify({'success':'You are loggged in as '+username,'authorization':token}))
            return res

@app.route('/api/v1/logout')
@ensure_user_logged_in
def get_logout():
    access.blacklist_token(g.token,g.token)
    return jsonify({"success":"you are logged out"}),200

#auth endpoints end here




#orders endpoints start here
@app.route('/api/v1/orders')
@ensure_admin_logged_in
def get_orders():
    return jsonify(orders.get_orders())

@app.route('/api/v1/orders/<order_id>')
@ensure_admin_logged_in
def get_order(order_id):
    order = orders.get_order_by_id(order_id)
    if not order is None:
        return jsonify({'status':'success','message':'Order Id is valid, list of all Orders attached',order_id:order}),200
    else:
        return jsonify({'status':'failed','message':'Order Id is invalid',order_id:None}),200

@app.route('/api/v1/orders/by/<client_id>')
@ensure_user_logged_in
def get_client_orders(client_id):
    return jsonify({client_id:orders.get_order_by_client_id(client_id)}),200

@app.route('/api/v1/orders', methods=['POST'])
@ensure_user_logged_in
def post_orders():
    if not "ordered_by" in request.form or not "total" in request.form or not "status" in request.form:
        return jsonify({'status':'error','message':'bad or corrupted data.'}),204
    else:
        ordered_by = request.form["ordered_by"]
        items = request.form["items"].split("##")
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
            return jsonify({'status':'success','message':'order added successfully'}),200
        else:
            return jsonify({'status':'error','message':'database error'}),400

@app.route('/api/v1/menu/remove', methods=['POST'])
@ensure_admin_logged_in
def remove_from_menu():
    if not "id" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    else:
        _id = request.form["id"]
        if not orders.get_menu_item(_id) is None:
            orders.remove_menu_item(_id)
            return jsonify({'success':'menu item '+_id+' deleted'}),200
        else:
            return jsonify({'error':'menu item '+_id+' does not exist'}),200
#menu endpoints end here



if __name__ == '__main__':
    app.run(use_realoader=True,threaded=True)
