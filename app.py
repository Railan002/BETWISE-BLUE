from flask import Flask, jsonify, render_template
from prediction import get_predictions

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predictions")
def predictions():
    return jsonify(get_predictions())

if __name__ == "__main__":
    app.run(debug=True)
