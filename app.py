import streamlit as st
import numpy as np
import pickle
import os

# ---------------- 1. Simple Pathing ---------------- #
# Since app.py and the .pkl files are in the SAME folder, 
# we just use the filename directly.
MODEL_FILE = "Rs.pkl"
PREP_FILE = "preprocessor.pkl"

# ---------------- 2. Background Styling ---------------- #
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
        background-size: cover;
    }
    label, h1 { color: black !important; font-weight: bold; }
    .result-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        color: black;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- 3. Load Models ---------------- #
@st.cache_resource
def load_models():
    # Double check if files exist in the current directory
    if not os.path.exists(MODEL_FILE) or not os.path.exists(PREP_FILE):
        return None, None
    
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    with open(PREP_FILE, "rb") as f:
        preprocessor = pickle.load(f)
    return model, preprocessor

model, preprocessor = load_models()

if model is None:
    st.error(f"Error: Could not find {MODEL_FILE} or {PREP_FILE} in the main folder.")
    st.info("Current files in folder: " + str(os.listdir(".")))
    st.stop()

# ---------------- 4. UI ---------------- #
st.title("🌾 Crop Yield Prediction")

col1, col2 = st.columns(2)
with col1:
    Area = st.text_input("Area")
    Item = st.text_input("Crop Type")
    Year = st.number_input("Year", 1990, 2030, 2024)
with col2:
    Rainfall = st.number_input("Rainfall (mm/year)")
    Temp = st.number_input("Temp (°C)")
    Pesticide = st.number_input("Pesticide (tonnes)")

if st.button("Predict Yield"):
    try:
        features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
        transformed = preprocessor.transform(features)
        prediction = model.predict(transformed)
        
        st.markdown(
            f"<div class='result-box'>Predicted Yield: {round(float(prediction[0]), 2)} hg/ha</div>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Prediction error: {e}")
