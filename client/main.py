import os
from flask import Flask, render_template
from CalcForm import CalcForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "minecraft"


@app.route("/", methods=["GET", "POST"])
def index():
    form = CalcForm()
    return render_template(
        "mainPage.html",
        form=form,
        expressions=['5 + 3 = 8', '5 - 3 = 2'],
        page=1,
        size=1,
        answer=25
    )


if __name__ == "__main__":  # Проверка прямого запуска.
    # Запуск программы.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
