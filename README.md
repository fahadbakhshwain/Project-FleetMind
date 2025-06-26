# Project FleetMind: End-to-End Car Rental Demand Prediction

![Bike Sharing](reports/figures/feature_importance.png)

## 1. Project Overview

This project is an end-to-end data science case study focused on predicting demand for a vehicle rental service (using a bike-sharing dataset as a proxy). The goal was to analyze historical data to understand key demand drivers and build a high-performance machine learning model to accurately forecast hourly rental counts.

The project demonstrates proficiency in data cleaning, exploratory data analysis (EDA), feature engineering, model building, and performance evaluation.

---

## 2. Key Findings & Insights

Our analysis revealed several critical factors influencing rental demand:

*   **Time is King:** The hour of the day is the single most important predictor, with clear peaks during morning (8 AM) and evening (5-6 PM) commute times.
*   **Weather is Crucial:** Temperature has the strongest positive correlation with demand, while humidity and poor weather conditions (rain/snow) are strong negative predictors.
*   **Seasonal Patterns:** Demand peaks in the Fall, suggesting that mild, pleasant weather is optimal for rentals, even more so than the summer heat.
*   **Business Growth:** A clear year-over-year growth in demand was observed, highlighting the service's expanding user base.

---

## 3. Machine Learning Model

After testing several models, a **Random Forest Regressor** was selected as the final model due to its superior performance.

*   **Performance Metrics:**
    *   **R-squared (R²): 0.94** (The model explains 94% of the variance in rental demand).
    *   **Mean Squared Error (MSE):** 1852.63

This high level of accuracy indicates that the model can be reliably used for operational planning, such as fleet distribution and dynamic pricing.

---

## 4. Tools & Technologies Used

*   **Language:** Python 3.9
*   **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn
*   **Environment:** Conda & Git
*   **IDE:** Visual Studio Code

---

## 5. Project Structure

The repository is organized as follows: