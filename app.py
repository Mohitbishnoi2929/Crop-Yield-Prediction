import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Crop Intelligence Hub", layout="wide")

# --- 2. BEAUTIFUL CROP BACKGROUND & STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Semi-transparent overlay for readability */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }
    [data-testid="stMetricValue"] { font-size: 24px; color: #f2a900 !important; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; }
    .result-box {
        background-color: rgba(242, 169, 0, 0.2);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #f2a900;
        text-align: center;
        font-size: 24px;
        color: #f2a900;
        font-weight: bold;
    }
    h1, h2, h3, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & MODEL LOADING ---
@st.cache_data
def load_data():
    file_path = "yield_df.csv"
    if not os.path.exists(file_path):
        st.error(f"Error: '{file_path}' not found.")
        st.stop()
    return pd.read_csv(file_path)

@st.cache_resource
def load_models():
    with open("Rs.pkl", "rb") as f:
        model = pickle.load(f)
    with open("preprocessor.pkl", "rb") as f:
        prep = pickle.load(f)
    return model, prep

df = load_data()
model, preprocessor = load_models()

# --- 4. TABS NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🔮 Yield Predictor", "🌍 Global Performance", "🌡️ Climate Impact"])

# ---------------- TAB 1: PREDICTOR ----------------
with tab1:
    st.title("🌾 Crop Yield Prediction")
    c1, c2 = st.columns(2)
    with c1:
        Area = st.selectbox("Select Country", sorted(df['Area'].unique()))
        Item = st.selectbox("Select Crop", sorted(df['Item'].unique()))
        Year = st.number_input("Year", 1990, 2030, 2024)
    with c2:
        Rainfall = st.number_input("Rainfall (mm/year)", value=1100.0)
        Temp = st.number_input("Avg Temp (°C)", value=20.0)
        Pesticide = st.number_input("Pesticide (tonnes)", value=100.0)

    if st.button("Predict Yield", use_container_width=True):
        features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
        transformed = preprocessor.transform(features)
        prediction = model.predict(transformed)
        st.markdown(f"<div class='result-box'>Predicted Yield: {round(float(prediction[0]), 2)} hg/ha</div>", unsafe_allow_html=True)

# ---------------- TAB 2: GLOBAL PERFORMANCE ----------------
with tab2:
    st.title("📊 Global Crop Performance")
    
    # KPI Row 1
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Yield", f"{df['hg/ha_yield'].sum()/1e9:.1f}B")
    k2.metric("Avg Yield", f"{int(df['hg/ha_yield'].mean())}")
    k3.metric("Countries", df['Area'].nunique())
    k4.metric("Crops", df['Item'].nunique())
    k5.metric("Pest. Eff.", "2.08") 
    k6.metric("Total Pest.", f"{df['pesticides_tonnes'].sum()/1e6:.1f}M")

    # Main Row
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.subheader("Crop-wise Yield vs Pesticide Usage")
        crop_agg = df.groupby('Item').agg({'hg/ha_yield':'mean', 'pesticides_tonnes':'mean'}).reset_index()
        fig1 = px.bar(crop_agg, x='Item', y=['hg/ha_yield', 'pesticides_tonnes'], barmode='group', template="plotly_dark", color_discrete_sequence=['#f2a900', '#1f77b4'])
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        top_bottom = st.radio("Show Countries:", ["Top 10", "Bottom 10"], horizontal=True)
        is_asc = True if top_bottom == "Bottom 10" else False
        country_yield = df.groupby('Area')['hg/ha_yield'].mean().sort_values(ascending=is_asc).head(10).reset_index()
        fig2 = px.bar(country_yield, x='hg/ha_yield', y='Area', orientation='h', template="plotly_dark", color_discrete_sequence=['#f2a900'])
        st.plotly_chart(fig2, use_container_width=True)

    # Bottom Row
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Yield Per Year (Trend)")
        yearly_yield = df.groupby('Year')['hg/ha_yield'].mean().reset_index()
        fig3 = px.area(yearly_yield, x='Year', y='hg/ha_yield', template="plotly_dark", color_discrete_sequence=['#f2a900'])
        st.plotly_chart(fig3, use_container_width=True)
    with c2:
        st.subheader("Yield Growth %")
        yearly_yield['Growth'] = yearly_yield['hg/ha_yield'].pct_change() * 100
        fig4 = px.line(yearly_yield, x='Year', y='Growth', template="plotly_dark", color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig4, use_container_width=True)

# ---------------- TAB 3: CLIMATE IMPACT ----------------
with tab3:
    st.title("🌡️ Climate Impact Dashboard")
    
    # KPIs for Climate
    ck1, ck2, ck3, ck4 = st.columns(4)
    ck1.metric("Avg Rainfall", f"{int(df['average_rain_fall_mm_per_year'].mean())} mm")
    ck2.metric("Avg Temp", f"{round(df['avg_temp'].mean(), 2)} °C")
    ck3.metric("Rain Efficiency", "67.06%")
    ck4.metric("Max Production", f"{int(df['hg/ha_yield'].max()/1000)}K")

    # Impact Charts
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("Yield vs Rainfall Trend")
        rain_trend = df.groupby('Year').agg({'hg/ha_yield':'mean', 'average_rain_fall_mm_per_year':'mean'}).reset_index()
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=rain_trend['Year'], y=rain_trend['hg/ha_yield'], name="Yield", fill='tozeroy'))
        fig5.add_trace(go.Scatter(x=rain_trend['Year'], y=rain_trend['average_rain_fall_mm_per_year'], name="Rainfall", yaxis="y2"))
        fig5.update_layout(template="plotly_dark", yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(fig5, use_container_width=True)
        
    with row1_col2:
        st.subheader("Impact of Rainfall on Yield")
        fig6 = px.scatter(df, x="average_rain_fall_mm_per_year", y="hg/ha_yield", color="Item", template="plotly_dark", opacity=0.5)
        st.plotly_chart(fig6, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.subheader("Yield vs Temp Trend")
        temp_trend = df.groupby('Year').agg({'hg/ha_yield':'mean', 'avg_temp':'mean'}).reset_index()
        fig7 = px.line(temp_trend, x="Year", y=["hg/ha_yield", "avg_temp"], template="plotly_dark")
        st.plotly_chart(fig7, use_container_width=True)
    with row2_col2:
        st.subheader("Impact of Temp on Yield")
        fig8 = px.scatter(df, x="avg_temp", y="hg/ha_yield", color="Item", template="plotly_dark", opacity=0.5)
        st.plotly_chart(fig8, use_container_width=True)
