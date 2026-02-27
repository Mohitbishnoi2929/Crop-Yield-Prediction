import streamlit as st

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("## 🚀 Navigate Through the Platform")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Prediction"):
        st.switch_page("Predictive_page.py")

with col2:
    if st.button("📊 Dashboard Overview"):
        st.switch_page("Dashboard_Overview.py")

with col3:
    if st.button("🌦 Climate Impact"):
        st.switch_page("Climate_Impact.py")
