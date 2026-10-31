import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sklearn.linear_model import LinearRegression

app = Flask(__name__, static_folder="ui")
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
regression_model = None
top_districts = []


def initialize_model_and_data():
    global regression_model, top_districts
    if not os.path.exists(DATA_PATH):
        print("⚠️ Warning: data.csv not found.")
        return

    try:
        df = pd.read_csv(DATA_PATH, sep=';')
        df.columns = df.columns.str.strip()
        daily_columns = df.columns[3:]
        df["MonthlyRainfall"] = df[daily_columns].sum(axis=1)

        np.random.seed(42)
        df["R"] = 0.5 * df["MonthlyRainfall"]
        df["K"] = np.random.uniform(0.2, 0.4, len(df))
        df["LS"] = np.random.uniform(1.0, 3.0, len(df))
        df["C"] = np.random.uniform(0.1, 0.6, len(df))
        df["P"] = 0.8
        df["SoilLoss"] = df["R"] * df["K"] * df["LS"] * df["C"] * df["P"]

        def classify_risk(loss):
            if loss < 20:
                return "Low"
            elif loss < 50:
                return "Moderate"
            elif loss < 100:
                return "High"
            else:
                return "Severe"

        df["Risk"] = df["SoilLoss"].apply(classify_risk)

        # Train Linear Regression model
        X = df[["MonthlyRainfall"]]
        y = df["SoilLoss"]
        model = LinearRegression()
        model.fit(X, y)
        regression_model = model

        # Cache top 10 districts
        top10_df = df.sort_values(by="SoilLoss", ascending=False).head(10)
        top_districts = top10_df[["state", "district", "MonthlyRainfall", "SoilLoss", "Risk"]].to_dict(orient="records")
        for d in top_districts:
            d["MonthlyRainfall"] = round(float(d["MonthlyRainfall"]), 1)
            d["SoilLoss"] = round(float(d["SoilLoss"]), 2)

        print("✅ RUSLE Linear Regression Model & District Rankings Loaded!")
    except Exception as e:
        print(f"Error initializing data: {e}")


# Initialize model on startup
initialize_model_and_data()


@app.route("/")
def serve_ui():
    return send_from_directory("ui", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("ui", path)


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json or {}
    try:
        rainfall = float(data.get("rainfall", 0))
        k = float(data.get("k", 0.3))
        ls = float(data.get("ls", 2.0))
        c = float(data.get("c", 0.4))
        p = float(data.get("p", 0.8))

        # Scientific RUSLE Calculation
        r = 0.5 * rainfall
        soil_loss = r * k * ls * c * p

        # ML Regression baseline comparison
        ml_estimate = None
        if regression_model:
            ml_estimate = float(regression_model.predict([[rainfall]])[0])

        if soil_loss < 20:
            risk = "Low"
            recommendation = "Maintain current crop and conservation practices. Soil stability is high."
        elif soil_loss < 50:
            risk = "Moderate"
            recommendation = "Increase canopy vegetation cover; introduce leguminous cover crops during fallow periods."
        elif soil_loss < 100:
            risk = "High"
            recommendation = "Implement contour farming, strip cropping, and organic mulching to retard surface runoff velocity."
        else:
            risk = "Severe"
            recommendation = "Immediate structural soil conservation required: bench terracing, check dams, and agroforestry buffers."

        return jsonify({
            "rainfall": rainfall,
            "soil_loss": round(soil_loss, 2),
            "ml_regression_estimate": round(ml_estimate, 2) if ml_estimate else None,
            "risk_level": risk,
            "recommendation": recommendation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/top-districts", methods=["GET"])
def get_top_districts():
    return jsonify(top_districts)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
