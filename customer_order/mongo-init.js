db.auth('comp3122', '23456')
db = db.getSiblingDB('customer_orders')

db.createCollection('Order')
db.Order.insertOne({
    'customer_id':1,
    'name': 'charlie',
    'order':[
        {'order_id':'r1o1', 'restaurant_id':1, 'food_id':1, 'taken':1},
        {'order_id':'r2o1', 'restaurant_id':2, 'food_id':3, 'taken':1},
        {'order_id':'r2o3', 'restaurant_id':2, 'food_id':3, 'taken':0}
    ]
})
db.Order.insertOne({
    'customer_id':2,
    'name': 'chloe',
    'order':[
        {'order_id':'r3o1', 'restaurant_id':3, 'food_id':3, 'taken':1},
        {'order_id':'r2o2', 'restaurant_id':2, 'food_id':2, 'taken':1},
        {'order_id':'r1o3', 'restaurant_id':1, 'food_id':2, 'taken':0}
    ]
})
db.Order.insertOne({
    'customer_id':3,
    'name': 'charlotte',
    'order':[
        {'order_id':'r3o2', 'restaurant_id':3, 'food_id':2, 'taken':1},
        {'order_id':'r1o2', 'restaurant_id':1, 'food_id':1, 'taken':0},
        {'order_id':'r3o3', 'restaurant_id':3, 'food_id':3, 'taken':0}
    ]
})