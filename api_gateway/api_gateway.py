import datetime
import flask
import hashlib
import json
import jwt
import pymongo
import redis
import requests


##############################
# Init library / connections
#######3######################
flask_app = flask.Flask(__name__)
mongo_client = pymongo.MongoClient('mongodb://comp3122:23456@user_db:27017')
redis_conn = redis.Redis(host='message_queue', port=6379)

####################
# Define functions 
####################

def hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def generate_token(user_info):
    return jwt.encode(user_info, "secretPassword", algorithm="HS256")

def authenticate_token(token):
    if not token:
        return None
    try:
        decode = jwt.decode(token, "secretPassword", algorithms=["HS256"], require=['id', 'group'])
    except:
        return None
    return decode

##########################
# Flask endpoints: login
##########################


@flask_app.route('/login', methods=['POST'])
def api_login():
    # Get login credentials
    username = flask.request.args.get('username')
    if not username:
        return {'error': 'username must be provided'}, 400
    password = flask.request.args.get('password')
    if not password:
        return {'error': 'password must be provided'}, 400
    username = username.lower()
    password = hash(password)

    # Get user information
    filter = {'username': username, 'password': password}
    db = mongo_client.user
    if result := db.customer.find_one(filter):
        user = {'id': result['id'], 'group': 'customer'}
    elif result := db.restaurant.find_one(filter):
        user = {'id': result['id'], 'group': 'restaurant'}
    elif result := db.delivery.find_one(filter):
        user = {'id': result['id'], 'group': 'delivery'}
    elif result := db.admin.find_one(filter):
        user = {'id': result['id'], 'group': 'admin'}
    else:
        return {'error': 'incorrect username or password'}, 404
    
    # Return token
    return {'token': generate_token(user)}, 200

#########################
# Flask endpoints: menu
#########################

@flask_app.route('/menu', methods=['GET'])
def get_menu():
    response = requests.get('http://menu:15000')
    return flask.jsonify(response.json()), response.status_code

@flask_app.route('/menu/<restaurant_id>', methods=['GET'])
def get_a_menu(restaurant_id):
    response = requests.get('http://menu:15000/'+restaurant_id)
    return flask.jsonify(response.json()), response.status_code

@flask_app.route('/menu/<restaurant_id>/<food_id>', methods=['GET'])
def get_a_food(restaurant_id, food_id):
    response = requests.get('http://menu:15000/'+restaurant_id+'/'+food_id)
    return flask.jsonify(response.json()), response.status_code

##########################
# Flask endpoints: order 
##########################
@flask_app.route('/order/<restaurant_id>', methods=['GET'])
def get_restaurant_order(restaurant_id):
    # Authentication token
    token = flask.request.args.get('token')
    if not token:
        return {'error': 'token is required'}, 400
    user = authenticate_token(token)
    if not user:
        return {'error': 'invalid token'}, 403
    if user['group'] != 'restaurant':
        return {'error': 'you do not have the permission to perform this request'}, 403
    if user['id'] != int(restaurant_id):
        return {'error': 'you do not have the permission to perform this request'}, 403
    
    # Perform request
    response = requests.get('http://restaurant_order:15000/'+restaurant_id)
    return flask.jsonify(response.json()), response.status_code


@flask_app.route('/order', methods=['POST'])
def post_order():
    # Authenticate token
    token = flask.request.args.get('token')
    if not token:
        return {'error': 'token is required'}, 400
    user = authenticate_token(token)
    if not user:
        return {'error': 'invalid token'}, 403
    if user['group'] != 'customer':
        return {'error': 'you do not have the permission to perform this request'}, 403
    
    # Check if food exists
    restaurant_id = flask.request.args.get('restaurant_id')
    if not restaurant_id:
        return {'error', 'restaurant_id is required'}, 400
    food_id = flask.request.args.get('food_id')
    if not food_id:
        return {'error', 'food_id is required'}, 400
    response = requests.get('http://menu:15000/'+restaurant_id+'/'+food_id)
    if response.status_code == 404:
        return flask.jsonify(response.json()), response.status_code
    
    order_id = hash(str(user['id'])+str(datetime.datetime.now().timestamp))

    load = json.dumps({
        'order_id': order_id,
        'user_id': user['id'],
        'restaurant_id': restaurant_id,
        'food_id': food_id
    })

    # Add order to restaurant
    redis_conn.publish('restaurantOrder_newOrder', load)
    redis_conn.publish('customerOrder_newOrder', load)
    return '200'


        

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True, port=15000)
