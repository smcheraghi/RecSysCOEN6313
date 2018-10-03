from flask import Flask, render_template, jsonify
from flask_cors import CORS
from random import *

app = Flask(__name__,
  static_folder = "./dist/static",
  template_folder = "./dist")

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/random', methods=['GET'])
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
