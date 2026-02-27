import streamlit as st
import os

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# Define the relative path
path_to_predictive = "pages/Predictive_page.py"

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        # Safety Check: If the file exists, switch. If not, show error on screen.
        if os.path.exists(path_to_predictive):
            st.switch_page(path_to_predictive)
        else:
            st.error(f"❌ File not found at: {path_to_predictive}")
            st.info("Ensure you have a folder named 'pages' in GitHub with 'Predictive_page.py' inside it.")

with col2:
    if st.button("📊 Dashboard Overview", use_container_width=True):
        st.write("Dashboard logic goes here")

with col3:
    if st.button("🌦 Climate Impact", use_container_width=True):
        st.write("Climate logic goes here")
