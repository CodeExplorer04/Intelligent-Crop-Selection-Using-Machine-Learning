import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data.csv", sep=';')

# Clean column names
df.columns = df.columns.str.strip()

# Daily rainfall columns
daily_columns = df.columns[3:]

# Monthly Rainfall
df["MonthlyRainfall"] = df[daily_columns].sum(axis=1)

# RUSLE Factors
np.random.seed(42)

df["R"] = 0.5 * df["MonthlyRainfall"]
df["K"] = np.random.uniform(0.2, 0.4, len(df))
df["LS"] = np.random.uniform(1.0, 3.0, len(df))
df["C"] = np.random.uniform(0.1, 0.6, len(df))
df["P"] = 0.8

# Soil Loss
df["SoilLoss"] = (
    df["R"]
    * df["K"]
    * df["LS"]
    * df["C"]
    * df["P"]
)

# Risk Classification
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

# Linear Regression
X = df[["MonthlyRainfall"]]
y = df["SoilLoss"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print(
    f"SoilLoss = {round(model.coef_[0],4)} × Rainfall + "
    f"{round(model.intercept_,4)}"
)

# Top 10 High Risk Districts
top10 = df.sort_values(
    by="SoilLoss",
    ascending=False
).head(10)

print(top10[
    ["state", "district", "SoilLoss", "Risk"]
])