import json
import redis
import requests

redis_conn = redis.Redis(host='message_queue', port=6379)

# Requests


def request_restaurant():
    response = requests.get('http://restaurant_order:15000/restaurant/1')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [{
        'restaurant_id': 1,
        'name': 'Hong Kong Happy Dim Sum',
        'order': [
            {'order_id': 'r1o1', 'customer_id': 1,
                'food_id': 1, 'perpare': 1, 'deliver': 1},
            {'order_id': 'r1o2', 'customer_id': 3,
                'food_id': 1, 'perpare': 1, 'deliver': 3},
            {'order_id': 'r1o3', 'customer_id': 2,
                'food_id': 2, 'perpare': 0, 'deliver': 0}
        ]
    }]


def request_order():
    response = requests.get('http://restaurant_order:15000/order/r1o1')
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": 1,
        "deliver": 1,
        "food_id": 1,
        "order_id": "r1o1",
        "perpare": 1,
        "restaurant_id": 1
    }

def test_new_order():
    data = json.dumps({
        'order_id': 'jjjj',
        'user_id': 1,
        'restaurant_id': 1,
        'food_id': 1
    })
    redis_conn.publish('restaurantOrder_newOrder', data)
    response = requests.get('http://restaurant_order:15000/order/jjjj')
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": 1,
        "deliver": 0,
        "food_id": 1,
        "order_id": "jjjj",
        "perpare": 0,
        "restaurant_id": 1
    }

def test_set_prepared():
    data = json.dumps({'order_id': "jjjj", 'prepared': 0})
    redis_conn.publish('restaurantOrder_setPrepared', data)
    response = requests.get('http://restaurant_order:15000/order/jjjj')
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": 1,
        "deliver": 0,
        "food_id": 1,
        "order_id": "jjjj",
        "perpare": 1,
        "restaurant_id": 1
    }

def test_set_shipped():
    data = json.dumps({'order_id': "jjjj", 'delivery_id': 3})
    redis_conn.publish('restaurantOrder_setShipped', data)
    response = requests.get('http://restaurant_order:15000/order/jjjj')
    assert response.status_code == 200
    assert response.json() == {
        "customer_id": 1,
        "deliver": 3,
        "food_id": 1,
        "order_id": "jjjj",
        "perpare": 1,
        "restaurant_id": 1
    }