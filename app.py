import streamlit as st
import numpy as np
import pickle

# load models
Rs = pickle.load(open('Rs.pkl','rb'))
preprocessor = pickle.load(open('preprocessor.pkl','rb'))

st.title("Crop Yield Prediction")

Area = st.text_input("Area")
Item = st.text_input("Item")
Year = st.number_input("Year")
Rainfall = st.number_input("Average Rainfall")
Temp = st.number_input("Average Temperature")
Pesticide = st.number_input("Pesticide in Tonnes")

if st.button("Predict"):
    features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
    transformed = preprocessor.transform(features)
    prediction = Rs.predict(transformed)

    st.success(f"Predicted Yield: {prediction[0]}")

