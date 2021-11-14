import datetime, flask, json, pymongo, redis
from flask.json import jsonify
from pymongo import MongoClient

##############################
# Init library / connections
##############################

flask_app = flask.Flask(__name__)
deliveries_coll = MongoClient('mongodb://comp3122:23456@delivery_order_db:27017', serverSelectionTimeoutMS=2000).delivery_orders.deliveries
redis_conn = redis.Redis(host='message_queue', port=6379)

################
# Redis events
################

def set_taken(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    taken = load['taken']
    orders = deliveries_coll.find_one({'orders.order_id': order_id})
    for order in orders["orders"]:
        if order['order_id'] == order_id:
            order["taken"] = taken
            break
    deliveries_coll.replace_one({'_id': orders['_id']}, orders)

def add_shipped(message):
    load = json.loads(message['data'])
    delivery = deliveries_coll.find_one({'delivery_id': load['delivery_id']})
    delivery['orders'].append({'order_id': load['order_id'], 'customer_id': load['customer_id'], 'restaurant_id': load['restaurant_id'], 'taken': 0})
    deliveries_coll.replace_one({'_id': delivery['_id']}, delivery)

###################
# Flask endpoints
###################

@flask_app.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    orders = deliveries_coll \
        .find_one({'orders.order_id': order_id}, { '_id': 0})['orders']
    for order in orders:
        if order['order_id'] == order_id:
            return order, 200
    return {'error': 'not found'}, 404

##############################
# Main: Run flask, establish subscription
##############################

if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'deliveryOrder_setTaken': set_taken})
    redis_pubsub.subscribe(**{'deliveryOrder_addShipped': add_shipped})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)

