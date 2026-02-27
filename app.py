import streamlit as st
import numpy as np
import pickle

# ------------------ Load Models ------------------ #
@st.cache_resource
def load_models():
    model = pickle.load(open("Rs.pkl", "rb"))
    preprocessor = pickle.load(open("preprocessor.pkl", "rb"))
    return model, preprocessor

Rs, preprocessor = load_models()

# ------------------ App UI ------------------ #
st.set_page_config(page_title="Crop Yield Prediction", layout="centered")

st.title("🌾 Crop Yield Prediction App")
st.write("Enter the details below to predict crop yield.")

# Input fields
Area = st.text_input("Area")
Item = st.text_input("Crop Type")
Year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
Rainfall = st.number_input("Average Rainfall (mm per year)", min_value=0.0)
Temp = st.number_input("Average Temperature (°C)")
Pesticide = st.number_input("Pesticide Used (tonnes)", min_value=0.0)

# ------------------ Prediction ------------------ #
if st.button("Predict Yield"):

    if Area and Item:
        try:
            features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
            transformed_features = preprocessor.transform(features)
            prediction = Rs.predict(transformed_features)

            st.success(f"✅ Predicted Crop Yield: {round(float(prediction[0]), 2)} hg/ha")

        except Exception as e:
            st.error("⚠️ Error in prediction. Please check model files and inputs.")
            st.exception(e)
    else:
        st.warning("⚠️ Please fill all required fields.")
