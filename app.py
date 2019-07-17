from flask import Flask, request, jsonify
from IPython import embed
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Flex's Microservice</h1>"

@app.route('/calories/<string:meal>/')
def calories(meal):
    qty = request.args['qty']
    headers = {
        'x-app-id': '4c066711',
        'x-app-key': 'bfc8f173bf0541073b4b219bd00d0ee6',
        'Content-Type': 'application/json'
    }

    data = {
     "query": meal,
     "timezone": "US/Eastern"
    }

    response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients/', json=data, headers=headers)
    food_data = json.loads(response.text)

    calories = food_data["foods"][0]["nf_calories"] / food_data["foods"][0]["serving_qty"] * float(qty)

    return jsonify({
        'calories': calories,
        'quantity': qty,
        'meal': meal
    })

if __name__ == '__main__':
    app.run(debug=True)
