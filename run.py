from flask import Flask, render_template, jsonify
from flask_cors import CORS
from random import *

app = Flask(__name__,
  static_folder = "./dist/static",
  template_folder = "./dist")

CORS(app, resources={r"/api/*": {"origins": "*"}})

# API routes
@app.route('/api/random', methods=['GET'])
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/test', methods=['GET'])
def api_test():
    response = {
        'key1': 'value1',
        'key2': 'value2'
    }
    return jsonify(response)

# Pages routes
@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
