# Calorie Coach API

This is a Flask app built with Python. It's purpose is to consume Nutritionx and Edamam endpoints and serve up JSON for an app that facilitates relationships between a Trainer and their Client. There are endpoints that retrieve meals based on restrictions and nutrients based on a meal look up.

This was jump into a non Rails framework. I learned a lot about how to translate what I know about MVC into a new space where convention is not guaranteed.

### Prerequisites

- python 3
- pip

Brew these up

### Installing

Clone Repo

```
cd flex_api

source venv/bin/activate

python3 api.py
```

'/meals?calories=100' serves a list of 100 recipes with a MAX of 100 calorie's per serving

Other param inputs:
'diet=high-protein'
'excluded=nuts'
'restriction=vegetarian'

Also a /food_info endpoint for retrieving macronutrients for searched meal

## Production

* [Thawing Lowlands](https://thawing-lowlands-89167.herokuapp.com)

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Pip 3](https://pip.pypa.io/en/stable/)

## Authors

* **Vince Carollo** - *All work* - [VinceCarollo](https://github.com/VinceCarollo)

## Endpoints

#### /food_info/pizza/?size=small

Returns macronutrients for meal given.

Input (params):
- Meal Name ('pizza'), Size(small, medium, large)

Response:
```
{
  calories: 213,
  carbs: 26,
  fats: 7,
  meal: "pizza",
  protein: 9,
  size: "small",
  sodium: 479,
  sugars: 2,
  thumbnail: "https://d2xdmhkmkbyw75.cloudfront.net/1060_thumb.jpg"
}
```

#### /meals?calories=200

Returns one hundred meals that meet requirements given.

Input (params):
- Calories (calorie max, required)
- Excluded (?excluded=nuts)
- Diet (?diet=balanced, or high_protein, etc.)
- Restriction (?restriction=vegan, or vegetarian)

Response:
```
{
  params: {
  calorie_max: "200",
  diet: "balanced",
  excluded: "None",
  restriction: "alcohol-free"
},
  recipes: [
  {
    calories_per_serving: 109,
    carbs_per_serving: 10,
    name: "Crispy Cheese Tacos Recipe",
    protein_per_serving: 4,
    servings: 8,
    thumbnail: "https://www.edamam.com/web-img/9fb/9fbdf8a084eb5fbbf8e116867a99e8cc.jpg",
    url: "http://www.seriouseats.com/recipes/2015/04/crispy-cheese-tacos-recipe.html"
  },
  {
    calories_per_serving: 133,
    carbs_per_serving: 17,
    name: "Vanilla Frozen Yogurt Recipe",
    protein_per_serving: 6,
    servings: 10,
    thumbnail: "https://www.edamam.com/web-img/146/146c072c175df9f407f9516a3f6466eb.jpg",
    url: "http://www.101cookbooks.com/archives/a-frozen-yogurt-recipe-to-rival-pinkberrys-recipe.html"
  }
]}
```
