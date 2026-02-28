import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Crop Intelligence Hub", layout="wide")

# --- 2. BACKGROUND & BLACK TEXT STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], 
    h1, h2, h3, p, label, .stSelectbox label, .stNumberInput label { 
        color: black !important; 
        font-weight: bold !important; 
    }
    .result-box {
        background-color: rgba(0, 0, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid black;
        text-align: center;
        font-size: 24px;
        color: black;
        font-weight: bold;
    }
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

# Function to force black axes on any plotly figure
def style_chrome(fig):
    fig.update_layout(
        font=dict(color="black"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='rgba(0,0,0,0.1)', tickfont=dict(color='black'), title_font=dict(color='black'))
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='rgba(0,0,0,0.1)', tickfont=dict(color='black'), title_font=dict(color='black'))
    return fig

# --- 4. TABS ---
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
    
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Prod.", f"{df['hg/ha_yield'].sum()/1e9:.1f}B")
    k2.metric("Avg Yield", f"{int(df['hg/ha_yield'].mean())}")
    k3.metric("Countries", df['Area'].nunique())
    k4.metric("Crops", df['Item'].nunique())
    k5.metric("Efficiency", "2.08") 
    k6.metric("Total Pest.", f"{df['pesticides_tonnes'].sum()/1e6:.1f}M")

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.subheader("Crop-wise Yield vs Pesticide Usage")
        crop_agg = df.groupby('Item').agg({'hg/ha_yield':'mean', 'pesticides_tonnes':'mean'}).reset_index()
        fig1 = px.bar(crop_agg, x='Item', y=['hg/ha_yield', 'pesticides_tonnes'], barmode='group', text_auto='.2s')
        st.plotly_chart(style_chrome(fig1), use_container_width=True)

    with col_r:
        top_bottom = st.radio("Rank Countries:", ["Top 10", "Bottom 10"], horizontal=True)
        is_asc = (top_bottom == "Bottom 10")
        country_yield = df.groupby('Area')['hg/ha_yield'].mean().sort_values(ascending=is_asc).head(10).reset_index()
        total_top_sum = country_yield['hg/ha_yield'].sum()
        country_yield['Percentage'] = (country_yield['hg/ha_yield'] / total_top_sum * 100).round(2)
        fig2 = px.bar(country_yield, x='hg/ha_yield', y='Area', orientation='h', text=country_yield['Percentage'].apply(lambda x: f'{x}%'))
        st.plotly_chart(style_chrome(fig2), use_container_width=True)

    st.subheader("Yield Distribution by Country")
    fig_map = px.choropleth(df, locations="Area", locationmode='country names', color="hg/ha_yield", color_continuous_scale="YlOrBr")
    fig_map.update_layout(font=dict(color="black"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Yield Per Year")
        yearly_yield = df.groupby('Year')['hg/ha_yield'].mean().reset_index()
        fig3 = px.line(yearly_yield, x='Year', y='hg/ha_yield', markers=True, text=yearly_yield['hg/ha_yield'].apply(lambda x: f'{x/1000:.1f}k'))
        fig3.update_traces(textposition="top center")
        st.plotly_chart(style_chrome(fig3), use_container_width=True)
    with c2:
        st.subheader("Yield Growth %")
        yearly_yield['Growth'] = (yearly_yield['hg/ha_yield'].pct_change() * 100).round(2)
        fig4 = px.line(yearly_yield.dropna(), x='Year', y='Growth', markers=True, text=yearly_yield['Growth'].dropna().apply(lambda x: f'{x}%'))
        fig4.update_traces(textposition="top center")
        st.plotly_chart(style_chrome(fig4), use_container_width=True)

# ---------------- TAB 3: CLIMATE IMPACT ----------------
with tab3:
    st.title("🌡️ Climate Impact Dashboard")
    
    ck1, ck2, ck3, ck4 = st.columns(4)
    ck1.metric("Avg Rainfall", f"{int(df['average_rain_fall_mm_per_year'].mean())} mm")
    ck2.metric("Avg Temp", f"{round(df['avg_temp'].mean(), 2)} °C")
    ck3.metric("Rain Efficiency", "67.06%")
    ck4.metric("Max Production", f"{int(df['hg/ha_yield'].max()/1000)}K")

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.subheader("Yield vs Rainfall Trend")
        rain_trend = df.groupby('Year').agg({'hg/ha_yield':'mean', 'average_rain_fall_mm_per_year':'mean'}).reset_index()
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=rain_trend['Year'], y=rain_trend['hg/ha_yield'], name="Yield", fill='tozeroy'))
        fig5.add_trace(go.Scatter(x=rain_trend['Year'], y=rain_trend['average_rain_fall_mm_per_year'], name="Rainfall", yaxis="y2"))
        fig5.update_layout(yaxis2=dict(overlaying='y', side='right', tickfont=dict(color='black')))
        st.plotly_chart(style_chrome(fig5), use_container_width=True)
    with r1c2:
        st.subheader("Impact of Rainfall on Yield")
        fig6 = px.scatter(df, x="average_rain_fall_mm_per_year", y="hg/ha_yield", color="Item", opacity=0.6)
        st.plotly_chart(style_chrome(fig6), use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.subheader("Yield vs Temperature Trend")
        temp_trend = df.groupby('Year').agg({'hg/ha_yield':'mean', 'avg_temp':'mean'}).reset_index()
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=temp_trend['Year'], y=temp_trend['hg/ha_yield'], name="Yield", line=dict(color='orange')))
        fig7.add_trace(go.Scatter(x=temp_trend['Year'], y=temp_trend['avg_temp'], name="Temp", yaxis="y2", line=dict(color='red')))
        fig7.update_layout(yaxis2=dict(overlaying='y', side='right', tickfont=dict(color='black')))
        st.plotly_chart(style_chrome(fig7), use_container_width=True)
    with r2c2:
        st.subheader("Impact of Temperature on Yield")
        fig8 = px.scatter(df, x="avg_temp", y="hg/ha_yield", color="Item", opacity=0.6)
        st.plotly_chart(style_chrome(fig8), use_container_width=True)
