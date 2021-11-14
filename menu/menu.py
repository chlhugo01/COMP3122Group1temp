import flask
import pymongo
#import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@menu_db:27017')
#redis_conn = redis.Redis(host='message_queue', port=6379)


##################
# Flask endpoints
##################

@flask_app.route('/', methods=['GET'])
def get_all_menu():
    db = mongo_client.menu.restaurants
    result = list(db.find({}, {'_id': 0}))
    return flask.jsonify(result)

@flask_app.route('/<restaurant_id>', methods=['GET'])
def get_a_restaurant(restaurant_id):
    db = mongo_client.menu.restaurants
    result = list(db.find({'id': int(restaurant_id)}, {'_id': 0}))
    return flask.jsonify(result)

@flask_app.route('/<restaurant_id>/<food_id>', methods=['GET'])
def get_a_food(restaurant_id, food_id):
    db = mongo_client.menu.restaurants
    result = list(db.find({'id': int(restaurant_id)}, {'_id': 0}))[0]['food']
    result = [food for food in result if food['id'] == int(food_id)]
    if not result:
        return {'error': 'food not found'}, 404
    return result[0], 200
    

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=15000)


