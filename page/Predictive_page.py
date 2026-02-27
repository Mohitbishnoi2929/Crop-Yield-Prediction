import streamlit as st
import numpy as np
import pickle

# ---------------- Page Setup ---------------- #
st.set_page_config(page_title="Crop Yield Prediction", layout="centered")

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

    input {
        color: black !important;
    }

    div[data-baseweb="input"] input {
        color: black !important;
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
    model = pickle.load(open("Rs.pkl", "rb"))
    preprocessor = pickle.load(open("preprocessor.pkl", "rb"))
    return model, preprocessor

model, preprocessor = load_models()

# ---------------- UI ---------------- #
st.title("🌾 Crop Yield Prediction")
st.write("Fill the details below to predict crop yield.")

Area = st.text_input("Area")
Item = st.text_input("Crop Type")
Year = st.number_input("Year", min_value=1900, max_value=2100)
Rainfall = st.number_input("Average Rainfall (mm/year)", min_value=0.0)
Temp = st.number_input("Average Temperature (°C)")
Pesticide = st.number_input("Pesticide Used (tonnes)", min_value=0.0)

# ---------------- Prediction ---------------- #
if st.button("Predict Yield"):
    if Area and Item:
        try:
            features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
            transformed = preprocessor.transform(features)
            prediction = model.predict(transformed)

            st.markdown(
                f"<div class='result-box'>Predicted Crop Yield: {round(float(prediction[0]), 2)} hg/ha</div>",
                unsafe_allow_html=True
            )

        except Exception:
            st.error("Prediction error occurred.")
    else:
        st.warning("Please fill all required fields.")

