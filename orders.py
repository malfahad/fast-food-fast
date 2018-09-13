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

    def updateStatus(self,status):
        self.status = status

    def json(self):
        return {'orderId':self.orderId,'orderedBy':self.by,'items':self.items,'status':self.status}
