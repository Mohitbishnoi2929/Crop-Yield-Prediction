import streamlit as st

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")

st.markdown("## 🚀 Navigate Through the Platform")

st.markdown("""
<div style="font-size:18px; line-height:2.2;">

<a href="/Predictive_page" 
title="Go to crop yield prediction page where you can input climate and soil data to predict yield"
style="text-decoration:none; color:black; font-weight:bold;">
🔮 Prediction
</a>

<br><br>

<a href="/Dashboard_Overview" 
title="View overall analytics and visual insights of crop production data"
style="text-decoration:none; color:black; font-weight:bold;">
📊 Dashboard Overview
</a>

<br><br>

<a href="/Climate_Impact" 
title="Analyze how rainfall, temperature and pesticides affect crop yield"
style="text-decoration:none; color:black; font-weight:bold;">
🌦 Climate Impact
</a>

</div>
""", unsafe_allow_html=True)
