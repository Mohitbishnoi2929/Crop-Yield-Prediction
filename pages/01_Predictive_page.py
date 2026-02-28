import streamlit as st
import numpy as np
import pickle
import os

# --- 1. SUPER ROBUST PATH LOGIC ---
# This finds the directory where THIS script is saved (the /pages folder)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# This moves UP one level to the main project folder
ROOT_DIR = os.path.dirname(CURRENT_DIR)

# Join the paths to the filenames (Case Sensitive!)
MODEL_PATH = os.path.join(ROOT_DIR, "Rs.pkl")
PREP_PATH = os.path.join(ROOT_DIR, "preprocessor.pkl")

# --- 2. LOAD MODELS ---
@st.cache_resource
def load_data():
    # Check if files exist before trying to open
    if not os.path.exists(MODEL_PATH):
        return None, f"Missing: {MODEL_PATH}"
    if not os.path.exists(PREP_PATH):
        return None, f"Missing: {PREP_PATH}"
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(PREP_PATH, 'rb') as f:
        preprocessor = pickle.load(f)
    return (model, preprocessor), None

data, error_msg = load_data()

if error_msg:
    st.error("🚨 Model files not found!")
    st.info(f"The app is looking for the files here: \n\n `{error_msg}`")
    st.warning("Please ensure Rs.pkl and preprocessor.pkl are in the same folder as app.py")
    st.stop()
else:
    model, preprocessor = data

# --- 3. UI & PREDICTION ---
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

if st.button("Predict"):
    try:
        features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
        transformed = preprocessor.transform(features)
        prediction = model.predict(transformed)
        st.success(f"Predicted Yield: {prediction[0]:.2f} hg/ha")
    except Exception as e:
        st.error(f"Prediction error: {e}")
