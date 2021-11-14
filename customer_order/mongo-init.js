db.auth('comp3122', '23456')
db = db.getSiblingDB('customer_orders')

db.createCollection('Order')
db.Order.insertOne({
    'customer_id':1,
    'name': 'charlie',
    'order':[
        {'order_id':'r1o1', 'restaurant_id':1, 'food_id':1, 'deliver':1,'taken':true},
        {'order_id':'r2o1', 'restaurant_id':2, 'food_id':3, 'deliver':3,'taken':true},
        {'order_id':'r2o3', 'restaurant_id':2, 'food_id':3, 'deliver':None,'taken':false}
    ]
})
db.Order.insertOne({
    'customer_id':2,
    'name': 'chloe',
    'order':[
        {'order_id':'r3o1', 'restaurant_id':3, 'food_id':3, 'deliver':2,'taken':true},
        {'order_id':'r2o2', 'restaurant_id':2, 'food_id':2, 'deliver':1,'taken':true},
        {'order_id':'r1o3', 'restaurant_id':1, 'food_id':2, 'deliver':None,'taken':false}
    ]
})
db.Order.insertOne({
    'customer_id':3,
    'name': 'charlotte',
    'order':[
        {'order_id':'r3o2', 'restaurant_id':3, 'food_id':2, 'deliver':2,'taken':true},
        {'order_id':'r1o2', 'restaurant_id':1, 'food_id':1, 'deliver':3,'taken':false},
        {'order_id':'r3o3', 'restaurant_id':3, 'food_id':3, 'deliver':None,'taken':false}
    ]
})