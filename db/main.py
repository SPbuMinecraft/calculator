import os

from flask import Flask, jsonify, abort, request

from CSVWorker import CSVWorker

app = Flask(__name__)

csv_worker = CSVWorker("db.csv")
csv_worker.add_first_line(['formula', 'answer'])

@app.route('/calculations/db', methods=['GET'])
def get_tasks():
    calculations = [[{'formula': computation[0], 'answer': computation[1].replace('\n', '')} for computation in csv_worker.get_lines()]]
    return jsonify({'calculations': calculations})


@app.route('/add', methods=['POST'])
def create_task():
    if not request.json or not 'formula' in request.json or not 'answer' in request.json:
        abort(400)
    
    csv_worker.add_line([request.json['formula'], request.json['answer']])
    return "done", 201

if __name__ == '__main__':
    app.run(port=6000, debug=True)
    # app.run(debug=True)