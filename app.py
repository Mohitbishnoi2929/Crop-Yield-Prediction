import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

# 2. UI Header
st.title("🌾 Crop Yield Analytics Platform")
st.markdown("## 🚀 Navigate Through the Platform")
st.divider()

# 3. Navigation Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### Prediction")
    st.write("Get AI-powered crop yield forecasts.")
    if st.button("Go to Prediction 🔮", use_container_width=True):
        # Note: If your file is in a folder named 'pages', use "pages/FileName.py"
        try:
            st.switch_page("pages/Predictive_page.py")
        except Exception:
            st.error("File not found. Ensure 'Predictive_page.py' is inside the 'pages' folder.")

with col2:
    st.info("### Dashboard")
    st.write("View historical trends and data insights.")
    if st.button("Go to Dashboard 📊", use_container_width=True):
        try:
            st.switch_page("pages/Dashboard_Overview.py")
        except Exception:
            st.error("File not found. Ensure 'Dashboard_Overview.py' is inside the 'pages' folder.")

with col3:
    st.info("### Climate")
    st.write("Analyze environmental impacts on yield.")
    if st.button("Go to Climate 🌦", use_container_width=True):
        try:
            st.switch_page("pages/Climate_Impact.py")
        except Exception:
            st.error("File not found. Ensure 'Climate_Impact.py' is inside the 'pages' folder.")
