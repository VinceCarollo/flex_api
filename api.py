from flask import Flask, request, jsonify, render_template
import requests
import json
import os
import environ

ROOT_PATH = os.path.abspath(__file__)
ENV_PATH = os.path.join(ROOT_PATH, '.env')

env = environ.Env(
    NUTRITIONX_ID=str,
    NUTRITIONX_KEY=str,
)

environ.Env.read_env(ENV_PATH)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Flex's Microservice</h1>"

@app.route('/food_info/<string:meal>/')
def calories(meal):
    size = request.args['size'].lower()
    headers = {
        'x-app-id': env('NUTRITIONX_ID'),
        'x-app-key': env('NUTRITIONX_KEY'),
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

        if food_data["foods"][0]["nf_sugars"].__class__.__name__ == 'NoneType':
            sugars = 0
        else:
            sugars    = int(food_data["foods"][0]["nf_sugars"] / food_data["foods"][0]["serving_qty"] * qty)

        calories  = int(food_data["foods"][0]["nf_calories"] / food_data["foods"][0]["serving_qty"])
        fats      = int(food_data["foods"][0]["nf_total_fat"] / food_data["foods"][0]["serving_qty"])
        protein   = int(food_data["foods"][0]["nf_protein"] / food_data["foods"][0]["serving_qty"])
        sodium   = int(food_data["foods"][0]["nf_sodium"] / food_data["foods"][0]["serving_qty"])
        carbs   = int(food_data["foods"][0]["nf_total_carbohydrate"] / food_data["foods"][0]["serving_qty"])
        thumbnail = food_data["foods"][0]["photo"]["thumb"]
        name = food_data["foods"][0]["food_name"]

        food_data = {
            'thumbnail': thumbnail,
            'calories': calories,
            'sugars': sugars,
            'fats': fats,
            'protein': protein,
            'sodium': sodium,
            'carbs': carbs,
            'size': size,
            'meal': meal
        }

        if meal == name:
            return jsonify(food_data)
        else:
            return render_template('meal_not_found.html'), 404
    except KeyError:
        return render_template('meal_not_found.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.run(debug=True)
