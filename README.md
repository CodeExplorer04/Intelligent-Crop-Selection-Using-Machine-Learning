# Soil Loss & Erosion Risk Prediction System

> **Scientific Soil Loss Estimation & Agricultural Conservation Advisory using RUSLE Modeling & Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Linear%20Regression-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Equation](https://img.shields.io/badge/Model-RUSLE%20Erosion%20Model-008080)](https://en.wikipedia.org/wiki/Universal_Soil_Loss_Equation)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

Soil erosion severely threatens agricultural productivity and land sustainability. The **Soil Loss & Erosion Risk Prediction System** combines meteorological data with the internationally recognized **Revised Universal Soil Loss Equation (RUSLE)** and **Linear Regression** modeling to predict regional soil loss rates and evaluate soil vulnerability.

The companion interactive web interface enables farmers, agronomists, and environmental planners to input local rainfall parameters, instantly calculate projected soil loss, determine erosion risk tiers, and receive actionable soil conservation recommendations.

---

## The Science: RUSLE Equation

The system models soil erosion using the Revised Universal Soil Loss Equation:

$$A = R \times K \times LS \times C \times P$$

Where:
- **$A$ (Soil Loss):** Estimated average annual soil loss (tons/hectare).
- **$R$ (Rainfall-Runoff Erosivity Factor):** Computed dynamically from daily/monthly rainfall datasets ($0.5 \times \text{Monthly Rainfall}$).
- **$K$ (Soil Erodibility Factor):** Soil susceptibility to detachment based on soil texture and organic matter.
- **$LS$ (Slope Length and Steepness Factor):** Topographical influence on erosion velocity.
- **$C$ (Cover-Management Factor):** Ground canopy and vegetation influence on soil shielding.
- **$P$ (Support Practice Factor):** Soil conservation techniques (contour plowing, strip cropping, terracing).

---

## Erosion Risk Classification

| Projected Soil Loss (t/ha) | Risk Level | Prescribed Agricultural Recommendation |
| :--- | :--- | :--- |
| **$< 20$** | **Low** | Maintain standard sustainable farming practices. |
| **$20 - 50$** | **Moderate** | Increase vegetation cover and utilize cover cropping. |
| **$50 - 100$** | **High** | Implement contour farming, strip cropping, and mulching. |
| **$\ge 100$** | **Severe** | Immediate structural soil conservation and terracing required. | ---

## Project Structure

```
Intelligent Crop Selection Using Machine Learning/
├── ui/
│   ├── index.html            # Web dashboard interface
│   ├── script.js             # Client-side RUSLE calculation & recommendation logic
│   └── style.css             # Responsive card-based UI stylesheet
├── soil.py                   # Data processing, RUSLE calculation, and Linear Regression
├── data.csv                  # Multi-region daily rainfall dataset
├── .gitignore                # Git exclusions
└── README.md                 # Project documentation
```

---

## Getting Started

### 1. Prerequisites
- Python 3.9+ installed
- Web browser (Chrome, Edge, Firefox, Safari)

### 2. Run the Machine Learning Script
```bash
# Navigate to the project directory
cd "Intelligent Crop Selection Using Machine Learning"

# Install required Python packages
pip install pandas numpy scikit-learn

# Execute the analysis and training model
python soil.py
```

**Script Output:**
- Calculates total monthly rainfall aggregated from multi-day precipitation readings.
- Computes RUSLE factors across all regional records.
- Fits a Linear Regression model: $\text{SoilLoss} = m \times \text{Rainfall} + c$.
- Identifies and prints the **Top 10 High Risk Districts** for targeted intervention.

### 3. Launch the Interactive Web Tool
Open `ui/index.html` directly in any web browser:
- Enter the state and district names.
- Provide the expected monthly rainfall in millimeters.
- Click **Predict Soil Loss** to view the projected soil loss, risk classification, and tailored agronomic recommendation.

---

## Sample Results

```
SoilLoss = 0.1245 × Rainfall + 3.4218

Top 10 High Risk Districts:
            state         district    SoilLoss      Risk
142    Maharashtra       Ratnagiri      148.22    Severe
87       Karnataka          Udupi      132.40    Severe
210         Kerala        Wayanad      115.65    Severe
```

---

## License

This project is licensed under the [MIT License](LICENSE).
