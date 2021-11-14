import flask
import pymongo
import json
import redis

##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@menu_db:27017')
redis_conn = redis.Redis(host='message_queue', port=6379)

db = mongo_client["menu"]
col = db["restaurants"]

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

def add_food(message):
    load = json.loads(message['data'])
    restaurant_id = load['restaurant_id']
    food_name = load['food_name']
    food_price = load['food_price']
    #new food
    foodresult = col.find_one({"id": int(restaurant_id)})
    query = {"_id" : foodresult["_id"] }
    lastid = col.find_one({"id": restaurant_id},{"_id":0,"food.id":1},sort=[("food.id",-1)])['food.id']
    foodresult["food"].append({'id':lastid+1, 'name':food_name, 'price':int(food_price)})
    col.replace_one( query, foodresult )

def delete_food(message):
    load = json.loads(message['data'])
    restaurant_id = load['restaurant_id']
    food_id = load['food_id']
    col.update( { "id" : int(restaurant_id) }, 
                 { "$pull" : { "food" : { "id" : int(food_id)}}})


if __name__ == '__main__':
    redis_pubsub = redis_conn.pubsub()
    redis_pubsub.subscribe(**{'menu_addFood': add_food})
    redis_pubsub.subscribe(**{'menu_deleteFood': delete_food})
    redis_pubsub_thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    flask_app.run(host='0.0.0.0', debug=True, port=15000)


