import datetime
import flask
import json
import pymongo
from pymongo import results
import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@customer_order_db:27017', serverSelectionTimeoutMS=2000)
redis_conn = redis.Redis(host='message_queue', port=6379)

db = mongo_client["customer_orders"]
col = db["Order"]

################
# Redis events
################

def new_order(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    restaurant_id = load['restaurant_id']
    food_id = load['food_id']
    customer_id = load['user_id']
    ### new order
    orderresult = col.find_one({"customer_id": int(customer_id)})
    query = {"_id" : orderresult["_id"] }
    orderresult["order"].append({'order_id':order_id, 'restaurant_id':restaurant_id, 'food_id':food_id, 'deliver':0,'taken':0})
    col.replace_one( query, orderresult )

###################
# Flask endpoints
###################

@flask_app.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    order = col \
        .find_one({'order.order_id': order_id}, { '_id': 0})['order']
    for x in order:
        if x['order_id'] == order_id:
            return x, 200
    return {'error': 'not found'}, 404

##############################
# Main: Run flask, establish subscription
#######3######################
if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'customerOrder_newOrder': new_order})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)

