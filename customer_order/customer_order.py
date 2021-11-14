import datetime
import flask
import json
import pymongo
import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@customer_order_db:27017')
redis_conn = redis.Redis(host='message_queue', port=6379)

db = mongo_client["customer_orders"]
order = db["Order"]

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
    orderresult = order.find_one({"customer_id": int(customer_id)})
    query = {"_id" : orderresult["_id"] }
    orderresult["order"].append({'order_id':order_id, 'restaurant_id':restaurant_id, 'food_id':food_id, 'deliver':0,'taken':0})
    order.replace_one( query, orderresult )

###################
# Flask endpoints
###################

@flask_app.route('/<restaurant_id>', methods=['GET'])
def get_a_restaurant(restaurant_id):
    db = mongo_client.restaurant_orders.restaurants
    result = list(db.find({'id': int(restaurant_id)}, {'_id': 0}))
    return flask.jsonify(result)

##############################
# Main: Run flask, establish subscription
#######3######################
if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'customerOrder_newOrder': new_order})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)

