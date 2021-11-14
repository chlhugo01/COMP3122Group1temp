db.auth('comp3122', '23456')
db = db.getSiblingDB('menu')

db.createCollection('restaurants');
db.restaurants.insertOne({
    'id': 1,
    'name': 'Hong Kong Happy Dim Sum',
    'food': [
        {'id': 1, 'name': 'Siu mai', 'price': 4},
        {'id': 2, 'name': 'Har Gao', 'price': 7},
        {'id': 3, 'name': 'Rice flour rool', 'price': 12}
    ]
})

db.restaurants.insertOne({
    'id': 2,
    'name': 'Hong Kong Happy Meal',
    'food': [
        {'id': 1, 'name': 'Chicken tart', 'price': 40},
        {'id': 2, 'name': 'Pork bun', 'price': 45},
        {'id': 3, 'name': 'Beef ball', 'price': 50}
    ]
})

db.restaurants.insertOne({
    'id': 3,
    'name': 'Hong Kong Happy Restaurant',
    'food': [
        {'id': 1, 'name': 'Curry rice', 'price': 24},
        {'id': 2, 'name': 'Hamburger', 'price': 30},
        {'id': 3, 'name': 'Rament', 'price': 40}
    ]
})