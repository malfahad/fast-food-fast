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

for i in range(6):
    m = menuItem("Fries","This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. This is a sample food description. ",10000,"http://placehold.it/100x100")
    add_menu_item(m)
