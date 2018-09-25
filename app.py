from flask import Flask,request,Response,send_from_directory,render_template,jsonify,make_response,abort
from flask_cors import CORS , cross_origin
import sessions
import orders
app = Flask(__name__)
CORS(app,expose_headers=["client-id","admin-client-id"])

Order = orders.Order
allOrders = orders.allOrders
MenuItem = orders.menuItem
menu = orders.Menu

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
        if sessions.adminLogin(username,password):
            #write cookie here
            res = make_response(jsonify({'success':'You are loggged in as admin'}))
            sessions.activate_admin_session()
            res.headers['admin-client-id'] = sessions.get_admin_session()
            #res.set_cookie("admin-client-id",value=sessions.get_unique_id())
            print res.headers
            return res
        else:
            return jsonify({'error':'incorrect username or password'})

@app.route('/api/v1/login', methods=['POST'])
def user_login():
    print request.form
    if not "username" in request.form or not "password" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    else:
        username = request.form["username"]
        password = request.form["password"]
        if not sessions.userLogin(username,password):
            return jsonify({'error':'invalid password or username'})
        else:
            #write cookie here
            res = make_response(jsonify({'success':'You are loggged in as admin'}))
            res.headers['client-id'] = value=sessions.getClientId(username)
            #res.set_cookie("client-id",value=sessions.getClientId(username))
            return res


@app.route('/api/v1/register', methods=['POST'])
def user_register():
    print request.form
    print request.headers
    if not "username" in request.form or not "password" in request.form or not "full name" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    else:
        full_name = request.form["full name"]
        username = request.form["username"]
        password = request.form["password"]
        if sessions.userExists(username):
            return jsonify({'error':'user already registered please login'})
        else:
            sessions.userRegister(full_name,username,password)
            #write cookie here
            res = make_response(jsonify({'success':'You are loggged in '}))
            res.headers['client-id'] = value=sessions.getClientId(username)
            #res.set_cookie("client-id",value=sessions.getClientId(username))
            print res.headers
            return res

@app.route('/api/v1/logout')
def get_logout():
    #read and destroy client_id
    if not request.headers.get('client-id') is None:
        id = request.headers.get('client-id')
        sessions.delete_session(id)
    return jsonify({"success":"you are logged out"})

@app.route('/api/v1/admin/logout')
def get_admin_logout():
    #read and destroy cookie
    sessions.destroy_admin_sess()
    return jsonify({"success":"you are logged out"})

@app.route('/api/v1/me')
def get_me():
    #read cookie and send session
    print request.headers
    if not request.headers.get('client-id') is None and not request.headers.get('client-id') is 'null':
        id = request.headers.get('client-id')
        userSession = sessions.get_session(id)
        if userSession == {}:
            print 'header client id '+request.headers.get('client-id')
            print 'server session with  client id '+str(sessions.get_session(id))
            abort(403)
        return jsonify({"success":"you are logged in","data":userSession})
    else:
        abort(403)

@app.route('/api/v1/admin/me')
def get_me_admin():
    #read cookie and send session
    print request.headers
    if not request.headers.get('admin-client-id') is 'null' and not sessions.get_admin_session() is None:
        #request.cookies.get('admin-client-id')
        if request.headers.get('admin-client-id') == sessions.get_admin_session():
            return jsonify({"success":"you are logged in","data":{"username":"admin"}})
        else:
            print 'header admin client id '+request.headers.get('admin-client-id')
            print 'server admin client id '+sessions.get_admin_session()
            abort(403)
    else:
        abort(403)
#auth endpoints end here




#orders endpoints start here
@app.route('/api/v1/orders')
def get_orders():
    return jsonify(allOrders)

@app.route('/api/v1/orders/<orderId>')
def get_order(orderId):
    if orderId in allOrders:
        return jsonify({orderId:allOrders[orderId]})
    else:
        return jsonify({orderId:None})



@app.route('/api/v1/orders/by/<clientId>')
def get_client_orders(clientId):
    return jsonify({clientId:fetchOrdersByClientId(clientId)})

@app.route('/api/v1/orders', methods=['POST'])
def post_orders():
    print request.form
    if not "orderedBy" in request.form or not "total" in request.form or not "status" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    else:
        orderedBy = request.form["orderedBy"]
        items = request.form["items"].split("##")
        total = request.form["total"]
        status = request.form["status"]
        order = Order(orderedBy)
        order.addItems(items)
        order.addTotal(total)
        order.updateStatus(status)
        allOrders[order.orderId] = order.json()
        return jsonify(allOrders[order.orderId])

@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
def put_order(orderId):
    if not "status" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
    elif not orderId in allOrders:
        return jsonify({'error':'unknown order Id.'})
    else:
        status = request.form["status"]
        allOrders[orderId]['status'] = status
        return jsonify({'success':'status updated to '+status})
#orders endpoints end here

#menu endpoints start here
@app.route('/api/v1/menu')
def get_menu():
    return jsonify(menu)

@app.route('/api/v1/menu', methods=['POST'])
def post_to_menu():
    if not "title" in request.form or not "desc" in request.form or not "amount" in request.form:
        return jsonify({'error':'bad or corrupted data.'})
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
        menuItem = MenuItem(title,desc,amount,img)
        menu[menuItem.id] = menuItem.json()
        return jsonify(menu[menuItem.id])

@app.route('/api/v1/menu/remove', methods=['POST'])
def remove_from_menu():
    res = make_response()
    if not "id" in request.form:
        return res(jsonify({'error':'bad or corrupted data.'}))
    else:
        _id = request.form["id"]
        if not menu.get(_id) is None:
            del menu[_id]
            return res(jsonify({'success':'menu item '+_id+' deleted'}))
        else:
            return res(jsonify({'error':'menu item '+_id+' does not exist'}))
#menu endpoints end here

def fetchOrdersByClientId(clientId):
    res = []
    for _id in allOrders.keys():
        if(allOrders[_id]['orderedBy'] == clientId):
            res.append(allOrders[_id])
    return res

if __name__ == '__main__':
    app.run(use_realoader=True,threaded=True)
