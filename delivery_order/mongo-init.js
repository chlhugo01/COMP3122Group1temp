db.auth('comp3122', '23456')
db = db.getSiblingDB('delivery_orders')

db.createCollection('deliveries')
db.deliveries.insertOne({
    'delivery_id':1,
    'name': 'daniel',
    'orders':[
        {'order_id':'r1o1','customer_id':1,'restaurant_id':1,'taken':1},
        {'order_id':'r2o2','customer_id':2,'restaurant_id':2,'taken':1}
    ]
})

db.deliveries.insertOne({
    'delivery_id':2,
    'name': 'daisy',
    'orders':[
        {'order_id':'r3o1', 'customer_id':2,'restaurant_id':3,'taken':1},
        {'order_id':'r3o2', 'customer_id':3,'restaurant_id':3,'taken':1}
    ]
})

db.deliveries.insertOne({
    'delivery_id':3,
    'name': 'dylan',
    'orders':[
        {'order_id':'r2o1', 'customer_id':1,'restaurant_id':2,'taken':1},
        {'order_id':'r1o2', 'customer_id':3,'restaurant_id':1,'taken':0}
    ]
})