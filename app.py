# app.py
from flask import Flask, request, jsonify, render_template
from exo1 import parcours_largeur, parcours_profondeur, shortest_path  # ton fichier python avec les algos

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/shortest_path", methods=["POST"])
def get_shortest_path():
    data = request.json
    start = data["start"]
    #end = data["end"]
    algo = data["algo"]
    
    path = shortest_path(algo, start)  # appelle ton algo de graphe
    return jsonify({"path": path})

if __name__ == "__main__":
    app.run(debug=True)
