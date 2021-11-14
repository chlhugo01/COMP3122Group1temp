import json
import redis
import requests
# from ..delivery_order import set_taken

redis_conn = redis.Redis(host='message_queue', port=6379)

def test_get_order():
    response = requests.get('http://delivery_order:15000/r1o1')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o1','customer_id':1,'restaurant_id':1,'taken':1
    }

def test_set_taken():
    data = json.dumps({'order_id': 'r1o1', 'taken': 0})
    redis_conn.publish('deliveryOrder_setTaken', data)
    response = requests.get('http://delivery_order:15000/r1o1')
    assert response.status_code == 200
    assert response.json() == {
        'order_id':'r1o1','customer_id':1,'restaurant_id':1,'taken':0
    }
    