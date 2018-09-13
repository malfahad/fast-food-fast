import pytest
from orders import Order,allOrders
from sessions import *

def test_order():
    o = Order('malende95@gmail.com')
    assert isinstance(o,Order), 'Order object should be of instance order'
    assert len(o.items) == 0,'Items length should be zero'
    o.addItems(['abc','def','geh','ijk','lmn'])
    assert len(o.items) == 5,'Items length should be five'
    allOrders[o.orderId] = o.json()
    o.status == 'CREATED'
    o.updateStatus('REJECTED')
    assert o.status == 'REJECTED'

def test_sessions():
    assert type(Users) == type({})
    assert 'admin' in admin
    x = adminLogin('admin','wrongpassword')
    assert x is False
    x = adminLogin('admin','admin')
    assert x is True
    x = userLogin('johndoe@gmail.com','1234')
    assert x is False
    userRegister('John Doe','johndoe@gmail.com','1234')
    assert userExists('johndoe@gmail.com')
    x = userLogin('johndoe@gmail.com','1234')
    assert x is True


test_order()
test_sessions()
print("All tests passed ")
