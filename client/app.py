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


@app.route("/", methods=('GET', 'POST'))
def index():
    form = CalcForm()
    answer = get_answer(form)
    history = get_history()

    return render_template(
        "mainPage.html",
        form=form,
        expressions=[
            f"{entry['question']} = {entry['answer']}" for entry in reversed(history)],
        answer=answer
    )


def get_answer(form: CalcForm):
    if form.is_submitted():
        json = {"question": form.expression.data}
        try:
            response = requests.post(
                SERVER_ADDRESS + "/calculate", json=json, timeout=3)
        except TimeoutError:
            return None
        if response.status_code == HTTPStatus.CREATED:
            return response.json()["answer"]
    return None  # TODO: show errors in UI


def get_history():
    try:
        responce = requests.get(SERVER_ADDRESS + "/history", timeout=3)
    except TimeoutError:
        return None
    if responce.status_code != HTTPStatus.OK:
        return None

    return responce.json()


if __name__ == "__main__":
    app.run(host="localhost", port=app.config["CLIENT_PORT"], debug=True)
