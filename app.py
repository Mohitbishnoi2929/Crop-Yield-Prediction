import streamlit as st

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        # NOTE: This string must match the filename in the 'pages' folder exactly
        st.switch_page("pages/Predictive_page.py")

with col2:
    if st.button("📊 Dashboard Overview", use_container_width=True):
        st.switch_page("pages/Dashboard_Overview.py")

with col3:
    if st.button("🌦 Climate Impact", use_container_width=True):
        st.switch_page("pages/Climate_Impact.py")
