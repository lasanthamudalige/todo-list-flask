from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


# Current year
# current_year = datetime.date.today().
# current_month = datetime.date.today().month
# current_day = datetime.date.today().day
date = datetime.today().strftime("%d/%m/%Y")


@app.route("/")
def home():
    print(date)
    return render_template("index.html", date=date)


if __name__ == "__main__":
    app.run()
