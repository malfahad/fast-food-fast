import uuid

all_orders = {}


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
        return {'order_id':self.order_id,'orderedBy':self.by,'items':self.items,'total':self.total,'status':self.status}

menu = {}

class MenuItem:
    def __init__(self,title,desc,amount,img):
        self.id = uuid.uuid4().hex
        self.title = title
        self.desc = desc
        self.amount = amount
        self.img = img
    def json(self):
        return {'id':self.id,'title':self.title,'desc':self.desc,'amount':self.amount,'img':self.img}

def add_menu_item(item):
    Menu[item.id] = item.json()

m = MenuItem("French Fries","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",10000,"http://placehold.it/200x200")
add_menu_item(m)
m = MenuItem("Fanta Soda","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",2000,"http://placehold.it/200x200")
add_menu_item(m)
m = MenuItem("Veg Burger","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",20000,"http://placehold.it/200x200")
add_menu_item(m)
m = MenuItem("Chicken Burger","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",15000,"http://placehold.it/200x200")
add_menu_item(m)
