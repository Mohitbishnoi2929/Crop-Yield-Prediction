import streamlit as st
import pickle
import os
import numpy as np

# --- 1. SETUP PATHS ---
# This ensures the script finds the files even when run from the root
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "..", "Rs.pkl")
preprocessor_path = os.path.join(current_dir, "..", "preprocessor.pkl")

# --- 2. LOAD MODELS ---
def load_data():
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(preprocessor_path, 'rb') as f:
        preprocessor = pickle.load(f)
    return model, preprocessor

try:
    model, preprocessor = load_data()
except FileNotFoundError:
    st.error("Error: Model files not found. Check if Rs.pkl is in the root folder.")
    st.stop()

# --- 3. PAGE UI ---
st.title("🔮 Predictive Analytics Page")
st.write("Enter the details below to get a prediction.")

# Example Input Fields (Adjust these to match your model's features)
feature_1 = st.number_input("Feature 1", value=0.0)
feature_2 = st.number_input("Feature 2", value=0.0)

if st.button("Predict"):
    # Prepare the input for the model
    # Note: Ensure the shape matches what your 'preprocessor' expects
    input_data = np.array([[feature_1, feature_2]])
    
    # Apply transformation if your preprocessor is a scaler/encoder
    transformed_data = preprocessor.transform(input_data)
    
    # Make Prediction
    prediction = model.predict(transformed_data)
    
    st.success(f"The predicted value is: {prediction[0]}")
