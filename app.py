# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Bike Rental Demand Predictor",
    page_icon="🚲",
    layout="centered"
)


# --- Load The Model ---
# This function will load our trained model
# @st.cache_data is a decorator that caches the model load, so it doesn't reload every time
@st.cache_data
def load_model():
    model_path = os.path.join('models', 'random_forest_demand_model.joblib')
    model = joblib.load(model_path)
    return model

model = load_model()


# --- App Title and Description ---
st.title("🚲 Bike Rental Demand Prediction App")
st.write(
    "This app uses a Random Forest model (R² Score: 0.94) to predict the hourly demand for bike rentals. "
    "Adjust the sliders and inputs below to get a prediction."
)
st.write("---")


# --- Create Input Fields in Two Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time & Season")
    # Input for Hour (hr)
    hour = st.slider("Hour of the Day (0-23)", 0, 23, 17) # Default to 5 PM
    # Input for Year (yr)
    year = st.selectbox("Year", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
    # Input for Month (mnth)
    month = st.selectbox("Month", options=range(1, 13))
    # Input for Weekday
    weekday = st.selectbox("Day of the Week", options=range(0, 7), format_func=lambda x: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][x])

with col2:
    st.subheader("Weather & Day Type")
    # Input for Weather Situation (weathersit)
    weather = st.selectbox("Weather Situation", options=[1, 2, 3, 4], format_func=lambda x: {1:"Clear", 2:"Mist/Cloudy", 3:"Light Rain/Snow", 4:"Heavy Rain/Snow"}[x])
    # Input for Temperature (temp) - Normalized value
    temp = st.slider("Temperature (Normalized)", 0.0, 1.0, 0.66, 0.01)
    # Input for Humidity (hum) - Normalized value
    hum = st.slider("Humidity (Normalized)", 0.0, 1.0, 0.60, 0.01)
    # Input for Holiday
    holiday = st.radio("Is it a holiday?", (0, 1), format_func=lambda x: "No" if x == 0 else "Yes")
    # Input for Working Day
    workingday = st.radio("Is it a working day?", (0, 1), format_func=lambda x: "No" if x == 0 else "Yes")
    windspeed = 0.19 # Using average windspeed as a constant for simplicity

# --- Prediction Logic ---
if st.button("Predict Demand"):
    # Create a DataFrame from the user's inputs
    # The order of columns MUST match the order used for training the model
    input_data = pd.DataFrame(
        [[year, month, hour, holiday, weekday, workingday, weather, temp, hum, windspeed]],
        columns=['yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'hum', 'windspeed']
    )
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    # Display the prediction
    st.success(f"Predicted Bike Rentals: **{int(prediction[0])}** rentals")