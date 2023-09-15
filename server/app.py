import requests
from datetime import datetime
from http import HTTPStatus
from flask import Flask, abort, request, Response
if __name__ == "__main__":
    from interpreter import Interpreter
else:
    from .interpreter import Interpreter

app = Flask(__name__)
app.config.from_pyfile("../config.py")

DB_ADDRESS = "http://" + app.config["DB_HOSTNAME"] + ":" + str(app.config["DB_PORT"])


def error(code: int, message: str):
    abort(Response(message, code))


@app.route('/calculate', methods=['POST'])
def create_task():
    if not request.json:
        error(HTTPStatus.BAD_REQUEST, message="No json provided")

    try:
        answer = Interpreter.evaluate(request.json['question'])
    except KeyError:
        error(HTTPStatus.BAD_REQUEST, message="Request must include a 'question'")
    except SyntaxError:
        error(HTTPStatus.BAD_REQUEST, message="Syntax error")
    except ArithmeticError:
        error(HTTPStatus.BAD_REQUEST, message="Division by 0?")
    except IndexError:
        error(HTTPStatus.BAD_REQUEST, message="Empty string is bAd")
    except Exception as e:
        error(HTTPStatus.BAD_REQUEST, message=str(e))
    
    if answer is None:
        error(HTTPStatus.BAD_REQUEST, message="Cannot evaluate this")

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

    return {"answer": answer, "saved": db_code == HTTPStatus.CREATED}, HTTPStatus.OK


@app.route('/history')
def get_tasks():
    try:
        responce = requests.get(DB_ADDRESS + "/history", timeout=3)
    except TimeoutError:
        error(HTTPStatus.REQUEST_TIMEOUT)
    if responce.status_code != HTTPStatus.OK:
        error(HTTPStatus.INTERNAL_SERVER_ERROR)
    return responce.json()


if __name__ == "__main__":
    app.run(host="localhost", port=app.config["SERVER_PORT"], debug=True)
