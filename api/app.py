from flask import Flask,request,Response,send_from_directory,render_template,jsonify
app = Flask(__name__)

import sessions
import orders
O = orders.Order
allOrders = orders.allOrders

# /api home
@app.route('/api/v1')
def home():
    return 'fast food fast api v1'

#auth endpoints
@app.route('/api/v1/admin/login', methods=['POST'])
def admin_login():
    if not "username" in request.get_json() or not "password" in request.get_json():
        return jsonify({'error':'bad or corrupted data.'})
    else:
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if sessions.adminLogin(username,password):
            #write cookie here
            return jsonify({'success':'You are loggged in as admin'})
        else:
            return jsonify({'error':'incorrect username or password'})

@app.route('/api/v1/login', methods=['POST'])
def user_login():
    print request.form
    if not "username" in request.form() or not "password" in request.form():
        return jsonify({'error':'bad or corrupted data.'})
    else:
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if not sessions.userLogin(username,password):
            return jsonify({'error':'invalid password or username'})
        else:
            return jsonify({'success':'You are loggged in as user'})

@app.route('/api/v1/register', methods=['POST'])
def user_register():
    if not "username" in request.get_json() or not "password" in request.get_json() or not "full name" in request.get_json():
        return jsonify({'error':'bad or corrupted data.'})
    else:
        full_name = request.get_json()["full name"]
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if sessions.userExists(username):
            return jsonify({'error':'user already registered please login'})
        else:
            sessions.userRegister(full_name,username,password)
            #add cookie here
            return jsonify({'success':'You are loggged in as user'})

@app.route('/api/v1/logout')
def get_logout():
    #read and destroy cookie
    return jsonify({"success":"you are logged out"})


#orders endpoints
@app.route('/api/v1/orders')
def get_orders():
    return jsonify(allOrders)

@app.route('/api/v1/orders/<orderId>')
def get_order(orderId):
    if orderId in allOrders:
        return jsonify({orderId:allOrders[orderId]})
    else:
        return jsonify({orderId:None})

@app.route('/api/v1/orders', methods=['POST'])
def post_orders():
    if not "orderedBy" in request.get_json() or not "items" in request.get_json() or not "status" in request.get_json():
        return jsonify({'error':'bad or corrupted data.'})
    else:
        orderedBy = request.get_json()["orderedBy"]
        items = request.get_json()["items"]
        status = request.get_json()["status"]
        o = O(orderedBy)
        o.addItems(items)
        o.updateStatus(status)
        allOrders[o.orderId] = o.json()
        return jsonify(allOrders[o.orderId])

@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
def put_order(orderId):
    if not "status" in request.get_json():
        return jsonify({'error':'bad or corrupted data.'})
    elif not orderId in allOrders:
        return jsonify({'error':'unknown order Id.'})
    else:
        status = request.get_json()["status"]
        allOrders[orderId]['status'] = status
        return jsonify({'success':'status updated to '+status})

if __name__ == '__main__':
    app.run(use_realoader=True,threaded=True)
