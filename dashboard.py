from flask import Flask, render_template
from models import PitchDeckData

app = Flask(__name__)

@app.route("/")
def dashboard():
    data = PitchDeckData.get_all_data()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)