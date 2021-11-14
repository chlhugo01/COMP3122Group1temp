db.auth('comp3122', '23456')
db = db.getSiblingDB('delivery_orders')

db.createCollection('Order')
db.Order.insertOne({
    'delivery_id':1,
    'name': 'daniel',
    'order':[
        {'order_id':'r1o1','customer_id':1,'restaurant_id':1,'taken':True},
        {'order_id':'r2o2','customer_id':2,'restaurant_id':2,'taken':True}
    ]
})
db.Order.insertOne({
    'delivery_id':2,
    'name': 'daisy',
    'order':[
        {'order_id':'r3o1', 'customer_id':2,'restaurant_id':3,'taken':True},
        {'order_id':'r3o2', 'customer_id':3,'restaurant_id':3,'taken':True}
    ]
})
db.Order.insertOne({
    'delivery_id':3,
    'name': 'dylan',
    'order':[
        {'order_id':'r2o1', 'customer_id':1,'restaurant_id':2,'taken':True},
        {'order_id':'r1o2', 'customer_id':3,'restaurant_id':1,'taken':False}
    ]
})