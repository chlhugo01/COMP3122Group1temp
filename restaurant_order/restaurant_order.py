import datetime
import flask
import pymongo

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@restaurant_order_db:27017')

##################
# Flask endpoints
##################

@flask_app.route('/<restaurant_id>', methods=['GET'])
def get_a_restaurant(restaurant_id):
    db = mongo_client.restaurant_orders.restaurants
    result = list(db.find({'id': int(restaurant_id)}, {'_id': 0}))
    return flask.jsonify(result)

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
    return {'order_id': id}, 202


##############################
# Main: Run flask
#######3######################
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=15000)

