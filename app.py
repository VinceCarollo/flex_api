from flask import Flask, request, jsonify, render_template
import config
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
        'x-app-id': config.nutritionx_id,
        'x-app-key': config.nutritionx_key,
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
        calories  = round(food_data["foods"][0]["nf_calories"] / food_data["foods"][0]["serving_qty"] * qty, 2)
        sugars    = round(food_data["foods"][0]["nf_sugars"] / food_data["foods"][0]["serving_qty"] * qty, 2)
        fats      = round(food_data["foods"][0]["nf_total_fat"] / food_data["foods"][0]["serving_qty"] * qty, 2)
        protein   = round(food_data["foods"][0]["nf_protein"] / food_data["foods"][0]["serving_qty"] * qty, 2)
        thumbnail = food_data["foods"][0]["photo"]["thumb"]
        name = food_data["foods"][0]["food_name"]

        food_data = {
            'thumbnail': thumbnail,
            'calories': calories,
            'sugars': sugars,
            'fats': fats,
            'protein': protein,
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
