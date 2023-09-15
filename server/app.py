import requests
from datetime import datetime
from http import HTTPStatus
from flask import Flask, abort, request
if __name__ == "__main__":
    from interpreter import Interpreter
else:
    from .interpreter import Interpreter

app = Flask(__name__)
app.config.from_pyfile("../config.py")

DB_ADDRESS = "http://" + app.config["DB_HOSTNAME"] + ":" + str(app.config["DB_PORT"])


@app.route('/calculate', methods=['POST'])
def create_task():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST, message="No json provided")

    try:
        answer = Interpreter.evaluate(request.json['question'])
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST, message="Request must include a 'question'")
    except SyntaxError:
        abort(HTTPStatus.BAD_REQUEST, message="Syntax error")
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, message="Division by 0?")

    calculation = {
        'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'question': request.json['question'],
        'answer': str(answer)
    }
    try:
        db_code = requests.post(DB_ADDRESS + "/add",
                                json=calculation, timeout=3).status_code
    except TimeoutError:
        db_code = HTTPStatus.REQUEST_TIMEOUT

    return {"answer": answer, "saved": db_code == HTTPStatus.CREATED}, db_code


@app.route('/history')
def get_tasks():
    try:
        responce = requests.get(DB_ADDRESS + "/history", timeout=3)
    except TimeoutError:
        abort(HTTPStatus.REQUEST_TIMEOUT)
    if responce.status_code != HTTPStatus.OK:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    return responce.json()


if __name__ == "__main__":
    app.run(host="localhost", port=app.config["SERVER_PORT"], debug=True)
