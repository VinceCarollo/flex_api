from flask import Flask, request, jsonify
from IPython import embed
from requests import request

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Flex's Microservice</h1>"

@app.route('/calories/<string:recipe>/')
def calories(recipe):
    qty = request.args['qty']
    r = requests.get('http://www.google.com')
    embed()
    return jsonify({
        'recipe': recipe,
        'quantity': qty
    })

if __name__ == '__main__':
    app.run(debug=True)
