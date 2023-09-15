import os
from enum import Enum
from flask import Flask, jsonify, abort, request

# from CSVWorker import CSVWorker
from SQLWorker import SQLWorker


class ErrorCode(Enum):
    STATUS_SUCCESS = 201
    STATUS_ERROR = 404


app = Flask(__name__)

# csv_worker = CSVWorker("db.csv")
sql_worker = SQLWorker("calculator.db")
# csv_worker.add_first_line(['formula', 'answer'])

@app.route('/calculations/db', methods=['GET'])
def get_tasks():
    calculations = [[{'formula': computation[0], 'answer': computation[1].replace('\n', '')} for computation in sql_worker.get_lines()]]
    return jsonify({'calculations': calculations})


@app.route('/add', methods=['POST'])
def create_task():
    if not request.json or not 'formula' in request.json or not 'answer' in request.json:
        abort(400)
    
    sql_worker.add_line([request.json['formula'], request.json['answer']])
    return "done", 201

if __name__ == '__main__':
    app.run(port=6000, debug=True)
    # app.run(debug=True)