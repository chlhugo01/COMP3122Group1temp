import json
import redis
import requests

redis_conn = redis.Redis(host='message_queue', port=6379)

def test_get_all_menu():
    response = requests.get('http://menu:15000')
    assert response.status_code == 200
    assert response.json() == [{
    'id': 1, 'name': 'Hong Kong Happy Dim Sum', 'food': [
        {'id': 1, 'name': 'Siu mai', 'price': 4},
        {'id': 2, 'name': 'Har Gao', 'price': 7},
        {'id': 3, 'name': 'Rice flour rool', 'price': 12}
    ]},
    {'id': 2,'name': 'Hong Kong Happy Meal','food': [
        {'id': 1, 'name': 'Chicken tart', 'price': 40},
        {'id': 2, 'name': 'Pork bun', 'price': 45},
        {'id': 3, 'name': 'Beef ball', 'price': 50}
    ]},
    {'id': 3,'name': 'Hong Kong Happy Restaurant','food': [
        {'id': 1, 'name': 'Curry rice', 'price': 24},
        {'id': 2, 'name': 'Hamburger', 'price': 30},
        {'id': 3, 'name': 'Rament', 'price': 40}
    ]
}]

def test_get_a_restaurant():
    response = requests.get('http://menu:15000/1')
    assert response.status_code == 200
    assert response.json() == [{
    'id': 1, 'name': 'Hong Kong Happy Dim Sum', 'food': [
        {'id': 1, 'name': 'Siu mai', 'price': 4},
        {'id': 2, 'name': 'Har Gao', 'price': 7},
        {'id': 3, 'name': 'Rice flour rool', 'price': 12}
    ]}]

def test_get_a_food():
    response = requests.get('http://menu:15000/1/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Siu mai', 'price': 4}

def test_add_food():
    load = json.dumps({'restaurant_id': 1, 'food_name':'bread','food_price': 10})
    redis_conn.publish('menu_addFood', load)
    response = requests.get('http://menu:15000/1/4')
    assert response.status_code == 200
    assert response.json() == {'id': 4, 'name': 'bread', 'price': 10}

def test_delete_food():
    load = json.dumps({'restaurant_id': 1, 'food_id': 4})
    redis_conn.publish('menu_deleteFood', load)
    response = requests.get('http://menu:15000/1')
    assert response.status_code == 200
    assert response.json() == [{
    'id': 1, 'name': 'Hong Kong Happy Dim Sum', 'food': [
        {'id': 1, 'name': 'Siu mai', 'price': 4},
        {'id': 2, 'name': 'Har Gao', 'price': 7},
        {'id': 3, 'name': 'Rice flour rool', 'price': 12}
    ]}]
    