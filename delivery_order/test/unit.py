import json, redis, requests, random

redis_conn = redis.Redis(host='message_queue', port=6379)

r_id = random.randint(1111,9999)
r_id_str = str(r_id)
def test_add_shipped():
    data = json.dumps({'delivery_id': 1, 'order_id': r_id_str,'customer_id': r_id,'restaurant_id': r_id})
    redis_conn.publish('deliveryOrder_addShipped', data)
    url = 'http://delivery_order:15000/' + r_id_str
    response = requests.get(url)
    assert response.status_code == 200

def test_set_taken():
    data = json.dumps({'order_id': r_id_str, 'taken': (r_id + 1)})
    redis_conn.publish('deliveryOrder_setTaken', data)
    url = 'http://delivery_order:15000/' + r_id_str
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {
        'order_id': r_id_str, 'customer_id': r_id, 'restaurant_id': r_id, 'taken': (r_id + 1)
    }