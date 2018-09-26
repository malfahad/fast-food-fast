import pytest
from orders import Order,all_orders
from sessions import *

def test_order():
    order = Order('malende95@gmail.com')
    assert isinstance(order,Order), 'Order object should be of instance order'
    assert len(order.items) == 0,'Items length should be zero'
    order.add_items(['abc','def','geh','ijk','lmn'])
    order.add_total(10000)
    assert len(order.items) == 5,'Items length should be five'
    all_orders[order.order_id] = order.json()
    order.status == 'CREATED'
    order.update_status('REJECTED')
    assert order.status == 'REJECTED'

def test_sessions():
    assert type(users) == type({})
    assert 'admin' in admin
    x = admin_login('admin','wrongpassword')
    assert x is False
    x = admin_login('admin','admin')
    assert x is True
    x = user_login('johndoe@gmail.com','1234')
    assert x is False
    user_register('John Doe','johndoe@gmail.com','1234')
    assert user_exists('johndoe@gmail.com')
    x = user_login('johndoe@gmail.com','1234')
    assert x is True
