import db
orders_db = db.OrdersDB()

class Order:
    def __init__(self,by):
        self.order_id = uuid.uuid4().hex
        self.items = []
        self.by =   by
        self.status = 'CREATED'

    def add_items(self,items):
        for item in items:
            self.items.append(item)
    def add_total(self,total):
        self.total = total

    def update_status(self,status):
        self.status = status

    def json(self):
        return {'order_id':orders_db.get_next_id(),'orderedBy':self.by,'items':self.items,'total':self.total,'status':self.status}
    def save(self):
        result =  orders_db.insert_order(self.json())

def get_orders():
    rows = orders_db.get_orders()
    result = {}
    if rows == None:
        return result
    for row in rows:
        result[row[0]] = {'order_id':row[0],
                          'ordered_by':row[1],
                          'items':row[2],
                          'total':row[3],
                          'status':row[4]}
    return result

def get_order_by_id(_id):
    rows = orders_db.get_order(_id)
    if rows == None:
        return rows
    elif len(rows) == 1:
        row = rows[0]
        return {'order_id':row[0],
                          'ordered_by':row[1],
                          'items':row[2],
                          'total':row[3],
                          'status':row[4]}
    else:
        return None

def get_order_by_for(_id):
    rows = orders_db.get_orders_by_username(_id)
    if rows == None:
        return result
    result = []
    for row in rows:
        result.append({'order_id':row[0],
                       'ordered_by':row[1],
                       'items':row[2],
                       'total':row[3],
                       'status':row[4]})
    return result

def update_order_status(_id,status):
    return orders_db.update_order_status(_id,status)
