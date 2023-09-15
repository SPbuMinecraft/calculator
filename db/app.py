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


@app.route('/add', methods=['POST'])
def create_task():
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
