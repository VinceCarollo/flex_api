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
