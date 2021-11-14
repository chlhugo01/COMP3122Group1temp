import json
import redis
import requests

redis_conn = redis.Redis(host='message_queue', port=6379)

def test_get_order():
    response = requests.get('http://customer_order:15000/r1o1')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o1', 'restaurant_id':1, 'food_id':1, 'deliver':1,'taken':1
    }

def test_new_order():
    load = json.dumps({'order_id': 'r1o4', 'restaurant_id':1,'food_id': 1,'user_id':1})
    redis_conn.publish('customerOrder_newOrder', load)
    response = requests.get('http://customer_order:15000/r1o4')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o4', 'restaurant_id':1, 'food_id':1, 'deliver':0,'taken':0
    }
    