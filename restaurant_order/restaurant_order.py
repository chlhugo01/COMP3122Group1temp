import datetime
import flask
import json
import pymongo
import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@restaurant_order_db:27017')
redis_conn = redis.Redis(host='message_queue', port=6379)

################
# Redis events
################

def new_order(message):
    load = json.loads(message['data'])
    order_id = load['order_id']
    restaurant_id = load['restaurant_id']
    food_id = load['food_id']
    user_id = load['user_id']
    ### new order

    


###################
# Flask endpoints
###################

@flask_app.route('/<restaurant_id>', methods=['GET'])
def get_a_restaurant(restaurant_id):
    db = mongo_client.restaurant_orders.restaurants
    result = list(db.find({'id': int(restaurant_id)}, {'_id': 0}))
    return flask.jsonify(result)
""" 
@flask_app.route('/', methods=['POST'])
def post_a_order():
    db = mongo_client.restaurant_orders.restaurants
    rows = db.collection.find({})
    id = len(list(rows))+1
    restaurant_id = flask.request.args.get('restaurant_id')
    food_id = flask.request.args.get('food_id')
    customer_id = flask.request.args.get('customer_id')
    db.insert_one({
        'id': id,
        'restaurant_id': restaurant_id,
        'food_id': food_id,
        'customer_id': customer_id,
        'datetime': str(datetime.datetime.now()),
        'prepared': False,
        'taken': False
    })
    id = 'R'+str(restaurant_id)+'O'+str(id)
    return flask.jsonify(rows), 200
    return {'order_id': id}, 202 """




##############################
# Main: Run flask, establish subscription
#######3######################
if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'restaurantOrder_newOrder': new_order})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)

