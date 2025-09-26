from flask import Flask, render_template, g
import database, os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "securelog.db")

def get_db():
    db = database.connect_db(DB_PATH)
    return db

@app.route("/")
def index():
    alerts = database.get_alerts(DB_PATH, limit=200)
    return render_template("index.html", alerts=alerts)

if __name__ == "__main__":
    # Initialize DB if not present
    database.init_db(DB_PATH)
    app.run(host="0.0.0.0", port=5000, debug=True)
