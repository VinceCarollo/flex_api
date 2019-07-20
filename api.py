from flask import Flask, request, jsonify, render_template
import requests
import json
import os
import environ
from pathlib import Path, PurePath

ROOT_PATH = Path.cwd()
ENV_PATH = os.path.join(ROOT_PATH, '.env')

env = environ.Env(
    NUTRITIONX_ID=str,
    NUTRITIONX_KEY=str,
    EDAMAM_ID=str,
    EDAMAM_KEY=str,
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

        calories  = int(food_data["foods"][0]["nf_calories"] / food_data["foods"][0]["serving_qty"] * qty)
        fats      = int(food_data["foods"][0]["nf_total_fat"] / food_data["foods"][0]["serving_qty"] * qty)
        protein   = int(food_data["foods"][0]["nf_protein"] / food_data["foods"][0]["serving_qty"] * qty)
        sodium    = int(food_data["foods"][0]["nf_sodium"] / food_data["foods"][0]["serving_qty"] * qty)
        carbs     = int(food_data["foods"][0]["nf_total_carbohydrate"] / food_data["foods"][0]["serving_qty"] * qty)
        thumbnail = food_data["foods"][0]["photo"]["thumb"]
        name      = food_data["foods"][0]["food_name"]

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

@app.route('/meals')
def meals():

    try:
        calorie_max = request.args['calories']
    except KeyError:
        return render_template('calories_required.html'), 404

    try:
        excluded = request.args['excluded']
    except KeyError:
        excluded = 'None'

    try:
        diet = request.args['diet']
    except KeyError:
        diet = 'balanced'

    try:
        constraints = request.args['constraints']
        if constraints == 'vegan':
            health = 'vegan'
        elif constraints == 'vegetarian':
            health = 'vegetarian'
        else:
            health = 'alcohol-free'
    except KeyError:
        health = 'alcohol-free'

    id = env('EDAMAM_ID')
    key = env('EDAMAM_KEY')

    response = requests.get(f'https://api.edamam.com/search?q=*&app_id={id}&app_key={key}&from=0&to=100&calories=0-{calorie_max}&excluded={excluded}&diet={diet}&health={health}')

    meal_data = json.loads(response.text)

    meals = {
        'params': {
            'calorie_max': calorie_max,
            'excluded': excluded,
            'diet': diet,
            'constraints': health
        },
        'recipes':[]
    }

    try:
        for meal in meal_data['hits']:
            name = meal['recipe']['label']
            thumbnail = meal['recipe']['image']
            url = meal['recipe']['url']
            servings = int(meal['recipe']['yield'])
            calories_per_serving = int(meal['recipe']['calories'] / servings)
            carbs_per_serving = int(meal['recipe']['digest'][1]['total'] / servings)
            protein_per_serving = int(meal['recipe']['digest'][2]['total'] / servings)

            meals['recipes'].append({
                'name': name,
                'thumbnail': thumbnail,
                'servings': servings,
                'url': url,
                'calories_per_serving': calories_per_serving,
                'carbs_per_serving': carbs_per_serving,
                'protein_per_serving': protein_per_serving
            })

    except KeyError:
        return render_template('meal_not_found.html'), 404

    return jsonify(meals)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('meal_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
