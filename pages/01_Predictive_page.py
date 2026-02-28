import streamlit as st
import numpy as np
import pickle
import os

# ---------------- Path Helper ---------------- #
# This finds the root directory even though this script is in /pages
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "Rs.pkl")
preprocessor_path = os.path.join(BASE_DIR, "preprocessor.pkl")

# ---------------- Background + Black Styling ---------------- #
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
        background-size: cover;
        background-position: center;
    }

    label {
        color: black !important;
        font-weight: bold;
    }

    h1 {
        color: black !important;
    }

    /* Prediction result box */
    .result-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        font-size: 20px;
        font-weight: bold;
        color: black;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Load Models ---------------- #
@st.cache_resource
def load_models():
    # Using the absolute paths we created above
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(preprocessor_path, "rb") as f:
        preprocessor = pickle.load(f)
    return model, preprocessor

try:
    model, preprocessor = load_models()
except FileNotFoundError:
    st.error(f"Could not find model files at {BASE_DIR}. Make sure Rs.pkl is in the main folder.")
    st.stop()

# ---------------- UI ---------------- #
st.title("🌾 Crop Yield Prediction")
st.write("Fill the details below to predict crop yield.")

# Use columns to make it look cleaner
col1, col2 = st.columns(2)

with col1:
    Area = st.text_input("Area (Country/Region)")
    Item = st.text_input("Crop Type (e.g., Maize)")
    Year = st.number_input("Year", min_value=1900, max_value=2100, value=2024)

with col2:
    Rainfall = st.number_input("Average Rainfall (mm/year)", min_value=0.0)
    Temp = st.number_input("Average Temperature (°C)", value=25.0)
    Pesticide = st.number_input("Pesticide Used (tonnes)", min_value=0.0)

# ---------------- Prediction ---------------- #
if st.button("Predict Yield"):
    if Area and Item:
        try:
            # Create features list
            features = [[Area, Item, Year, Rainfall, Temp, Pesticide]]
            
            # Transform and Predict
            transformed = preprocessor.transform(features)
            prediction = model.predict(transformed)

            st.markdown(
                f"<div class='result-box'>Predicted Crop Yield: {round(float(prediction[0]), 2)} hg/ha</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.warning("Please fill all required fields.")
