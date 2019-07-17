from flask import Flask, request, jsonify, render_template
from IPython import embed
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Flex's Microservice</h1>"

@app.route('/food_info/<string:meal>/')
def calories(meal):
    size = request.args['size'].lower()
    headers = {
        'x-app-id': 'f0f958da',
        'x-app-key': 'b2321d5535340e8928c1ea9e6b0ff7de',
        'Content-Type': 'application/json'
    }

    data = {
     "query": meal,
     "timezone": "US/Eastern"
    }

    qty = 0
    if size == 'small':
        qty = 0.75
    elif size == 'medium':
        qty = 1
    elif size == 'large':
        qty = 2
    else:
        return render_template('size_error.html')

    response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients/', json=data, headers=headers)
    food_data = json.loads(response.text)
    try:
        if food_data["foods"]:
            calories = round(food_data["foods"][0]["nf_calories"] / food_data["foods"][0]["serving_qty"] * qty, 2)
            name = food_data["foods"][0]["food_name"]

            food_data = {
                'calories': calories,
                'size': size,
                'meal': meal
            }

            if meal == name:
                return jsonify(food_data)
            else:
                return render_template('meal_not_found.html')
    except KeyError:
        return render_template('meal_not_found.html')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run(debug=True)