import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["file"]

    df = pd.read_csv(file)

    # solo columnas numéricas
    numeric = df.select_dtypes(include=["number"])

    if numeric.empty:
        return jsonify({"error":"No numeric columns found"})

    stats = {
        "columns": list(numeric.columns),
        "mean": numeric.mean().tolist(),
        "max": numeric.max().tolist(),
        "min": numeric.min().tolist()
    }

    return jsonify(stats)
#Vercel
app = app


