from flask import jsonify,g,request
from models import orders
from utils.access import Access

access = Access('my-secret-key')

class OrdersController:
    def __init__(self):
        pass
    def get_orders(self):
        if g.user_type == 'admin':
            data = orders.get_orders()
        else:
            data = orders.get_orders_for(g.user)
        message = 'you may have some orders' if len(data.keys())!=0 else 'There are no orders in the database'
        return jsonify({'status':'success','message':message,'data':data}),200

    def get_single_order(self,order_id):
        order = orders.get_order_by_id(order_id)
        if order is None:
            return jsonify({'status':'failed','message':'Order Id is invalid',order_id:None}),200
        else:
            if g.user_type != 'admin' and order['ordered_by'] != g.user:
                abort(405);#this is not your order. to be replaced with error handler
            return jsonify({'status':'success','message':'Order Id is valid, list of all Orders attached','data':{order_id:order}}),200

    def add_new_order(self,data):
        if data is None:
            return jsonify({'error':'No Json Data received. '}), 400
        if not "ordered_by" in data or not "total" in data  or not "items" in data:
            return jsonify({'status':'error','message':'missing required field.'}),400
        else:
            ordered_by = data["ordered_by"].strip()
            items = data["items"]
            total = data["total"]
            order = orders.Order(ordered_by)
            order.add_items(items)
            order.add_total(total)
            dbresult = order.save()
            if dbresult:
                return jsonify({'status':'success','message':'order added successfully'}),200
            else:
                return jsonify({'status':'error','message':'database error'}),400
    def update_order_status(self,order_id,data):
        if data is None:
            return jsonify({'error':'No Json Data received. '}), 400
        if not "status" in data:
            return jsonify({'error':'missing required field '})
        try:
            order_id = int(order_id)
        except:
            return jsonify({'error':'order id must be a number '})

        status = data["status"].strip().upper()
        statuses = ['CREATED','ACCEPTED','COMPLETED','REJECTED']
        if not status in statuses:
            return jsonify({'error':'status not among valid statuses '+str(statuses)})
        elif orders.get_order_by_id(order_id) is None:
            return jsonify({'error':'unknown order Id.'})
        else:
            status = data["status"]
            orders.update_order_status(order_id,status)
            return jsonify({'success':'status updated to '+status}),200
