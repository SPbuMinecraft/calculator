import requests

from flask import Flask, jsonify, abort, request
from urllib.parse import urlparse
from calculations import formula_parsing

app = Flask(__name__)

@app.route('/calculations', methods=['GET'])
def get_tasks():
    return requests.get('http://localhost:6000//calculations/db').json(), 201

@app.route('/calculate', methods=['POST'])
def create_task():
    if not request.json or not 'formula' in request.json:
        abort(400)
    
    exist, answer = formula_parsing(request.json['formula'])
    if exist:
        calculation = {
            'formula': request.json['formula'],
            'answer' : str(answer)
        }
        res = requests.post('http://localhost:6000//add', json=calculation)
        return answer, res.status_code
    else:
        return -1, 404

if __name__ == '__main__':
    app.run(debug=True)
