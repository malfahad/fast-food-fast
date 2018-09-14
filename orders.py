import uuid

allOrders = {}

class Order:
    def __init__(self,by):
        self.orderId = uuid.uuid4().hex
        self.items = []
        self.by =   by
        self.status = 'CREATED'

    def addItems(self,items):
        for item in items:
            self.items.append(item)
    def addTotal(self,total):
        self.total = total

    def updateStatus(self,status):
        self.status = status

    def json(self):
        return {'orderId':self.orderId,'orderedBy':self.by,'items':self.items,'total':self.total,'status':self.status}

Menu = {}

class menuItem:
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

m = menuItem("French Fries","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",10000,"http://placehold.it/200x200")
add_menu_item(m)
m = menuItem("Fanta Soda","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",2000,"http://placehold.it/200x200")
add_menu_item(m)
m = menuItem("Veg Burger","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",20000,"http://placehold.it/200x200")
add_menu_item(m)
m = menuItem("Chicken Burger","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",15000,"http://placehold.it/200x200")
add_menu_item(m)
