from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# データ保存（簡易：メモリ）
meal_data = {}

def get_week(start_date):
    return [start_date + timedelta(days=i) for i in range(7)]

@app.route("/", methods=["GET", "POST"])
def index():
    today = datetime.today()
    selected_date_str = request.args.get("date")

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
    else:
        selected_date = today

    # 日曜日スタートにする
    start_of_week = selected_date - timedelta(days=selected_date.weekday() + 1 if selected_date.weekday() != 6 else 0)

    week = get_week(start_of_week)

    if request.method == "POST":
        key = request.form["key"]
        meal_data[key] = not meal_data.get(key, True)
        return redirect(url_for("index", date=selected_date.strftime("%Y-%m-%d")))

    return render_template("index.html", week=week, meal_data=meal_data, selected_date=selected_date.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    app.run(debug=True)