<<<<<<< HEAD
from http import HTTPStatus
from csv import Error as CSVError
from flask import Flask, abort, request, Response
if __name__ == "__main__":
    from CSVWorker import CSVWorker
else:
    from .CSVWorker import CSVWorker

app = Flask(__name__)
app.config.from_pyfile("../config.py")

csv_worker = CSVWorker("db.csv")
csv_worker.add_first_line(["date", "question", "answer"])


def error(code: int, message: str):
    abort(Response(message, code))
=======
import os
from enum import Enum

from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<{self.expression} = {self.result}>'


class SQLWorker:
    def __init__(self, buffer_size: int = 1, clear_file: bool = True):
        with app.app_context():
            self.buffer_capacity = buffer_size
            self.buffer_size = 0
            if clear_file:
                db.drop_all()
                db.create_all()

    def add_line(self, line: list[str]):
        with app.app_context():
            db.session.add(Calculation(expression=line[0], result=line[1]))
            self.buffer_size += 1
            if self.buffer_size == self.buffer_capacity:
                db.session.commit()
                self.buffer_size = 0
    
    def get_lines(self):
        with app.app_context():
            return Calculation.query.all()


sql_worker = SQLWorker()

@app.route('/calculations/db', methods=['GET'])
def get_tasks():
    calculations = [[{'formula': computation.expression, 'answer': computation.result.replace('\n', '')} for computation in sql_worker.get_lines()]]
    return jsonify({'calculations': calculations})
>>>>>>> 7dfabe8 (Performs renaming)


@app.route('/add', methods=['POST'])
def create_task():
<<<<<<< HEAD
    json = request.json
    if not json:
        error(HTTPStatus.BAD_REQUEST, message="No json provided")
    try:
        csv_worker.add_line([json["date"], json["question"], json["answer"]])
    except KeyError as e:
        error(HTTPStatus.BAD_REQUEST, message=str(e))
    except CSVError as e:
        error(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
    return "done", HTTPStatus.CREATED


@app.route('/history')
def get_tasks():
    try:
        calculations = [
            {'date': line[0],
             'question': line[1],
             'answer': line[2].replace('\n', '')
             } for line in csv_worker.get_lines()
        ]
    except CSVError as e:
        error(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
    return calculations


if __name__ == "__main__":
    app.run(host="localhost", port=app.config["DB_PORT"], debug=True)
=======
    if not request.json or not 'formula' in request.json or not 'answer' in request.json:
        abort(400)
    
    sql_worker.add_line([request.json['formula'], request.json['answer']])
    return "done", 201

if __name__ == '__main__':
    app.run(port=6000, debug=True)
    # app.run(debug=True)
>>>>>>> 7dfabe8 (Performs renaming)
