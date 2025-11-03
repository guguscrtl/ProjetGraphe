from flask import Flask, request, jsonify, render_template
from exo1 import shortest_path

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shortest_path", methods=["POST"])
def get_shortest_path():
    data = request.json
    start = int(data.get("start", 0))
    end = int(data.get("end", 0))
    algo = data["algo"]

    result = shortest_path(algo, start, end)
    return jsonify(result) 

if __name__ == "__main__":
    app.run(debug=True)
