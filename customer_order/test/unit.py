import json
import redis
import requests

redis_conn = redis.Redis(host='message_queue', port=6379)

def test_get_order():
    response = requests.get('http://customer_order:15000/r1o1')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o1', 'restaurant_id':1, 'food_id':1, 'taken':1
    }

def test_get_null():
    response = requests.get('http://customer_order:15000/r1o5')
    assert response.status_code == 404
    assert response.json() == {'error': 'not found'}

def test_set_taken():
    data = json.dumps({'order_id': 'r2o3', 'taken': 1})
    redis_conn.publish('customerOrder_setTaken', data)
    response = requests.get('http://customer_order:15000/r2o3')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r2o3', 'restaurant_id':2, 'food_id':3, 'taken':1
    }

def test_new_order():
    load = json.dumps({'order_id': 'r1o4', 'restaurant_id':1,'food_id': 1,'user_id':1})
    redis_conn.publish('customerOrder_newOrder', load)
    response = requests.get('http://customer_order:15000/r1o4')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o4', 'restaurant_id':1, 'food_id':1, 'taken':0
    }


    