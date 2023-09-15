import requests
from http import HTTPStatus
from flask import Flask, render_template
if __name__ == "__main__":
    from CalcForm import CalcForm
else:
    from .CalcForm import CalcForm

app = Flask(__name__)
app.config.from_pyfile("../config.py")

SERVER_ADDRESS = "http://" + \
    app.config["SERVER_HOSTNAME"] + ":" + str(app.config["SERVER_PORT"])


class ServerException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.route("/", methods=('GET', 'POST'))
def index():
    form = CalcForm()
    answer = error = None
    try:
        answer = get_answer(form)
    except ServerException as e:
        error = e.message
    history = get_history()

    return render_template(
        "index.html",
        form=form,
        expressions=[
            f"{entry['question']} = {entry['answer']}" for entry in reversed(history)],
        answer=answer,
        error=error
    )


def get_answer(form: CalcForm):
    if form.is_submitted():
        json = {"question": form.expression.data}
        try:
            response = requests.post(
                SERVER_ADDRESS + "/calculate", json=json, timeout=3)
        except TimeoutError:
            return None
        if response.status_code == HTTPStatus.OK:
            return response.json()["answer"]
        raise ServerException(response.text)
    return None


def get_history():
    try:
        responce = requests.get(SERVER_ADDRESS + "/history", timeout=3)
    except TimeoutError:
        return []
    if responce.status_code != HTTPStatus.OK:
        return []

    return responce.json()['calculations']


if __name__ == "__main__":
    app.run(host="localhost", port=app.config["CLIENT_PORT"], debug=True)
