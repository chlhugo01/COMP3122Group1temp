import json
import redis
import requests

redis_conn = redis.Redis(host='message_queue', port=6379)

def test_get_order():
    response = requests.get('http://delivery_order:15000/r1o1')
    assert response.status_code == 200
    assert response.json() == {
        'delivery_id':1,
        'name': 'daniel',
        'order':[   {'order_id':'r1o1','customer_id':1,'restaurant_id':1,'taken':1},
                    {'order_id':'r2o2','customer_id':2,'restaurant_id':2,'taken':1}]
    }

""" def test_basic():
    data = {'order_id': 'r1o1', 'taken': 0}
    data_str = json.dumps(data)

    redis_conn.publish('deliveryOrder_setTaken', data_str)

    assert set_taken(message) == ('r1o1', 0) """