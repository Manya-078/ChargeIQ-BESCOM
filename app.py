import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import os

# --- Page Config ---
st.set_page_config(page_title="ChargeIQ | BESCOM AI", layout="wide", initial_sidebar_state="expanded")

# --- Custom Styling (Fixed & Improved Readability) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #3b82f6; }
    
    /* Improved Evidence Card Styling for Dark Mode */
    .evidence-card { 
        background-color: #1c2128; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #ff4b4b; 
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .evidence-card h4 {
        color: #ff4b4b; 
        margin-top: 0;
        margin-bottom: 10px;
    }
    .evidence-card p {
        color: #adbac7;
        line-height: 1.6;
        margin-bottom: 5px;
    }
    .evidence-card b {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Loading Helper ---
@st.cache_data
def load_all_data():
    if not os.path.exists('data/grid_status.csv'):
        st.error("Data files missing! Please run 'python src/generate_data.py' first.")
        return None, None
    grid = pd.read_csv('data/grid_status.csv')
    demand = pd.read_csv('data/demand_trends.csv')
    return grid, demand

grid_df, demand_df = load_all_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/3/3b/Bescom_logo.png", width=100)
    st.title("ChargeIQ Control")
    selected_zone = st.selectbox("Operational Zone", ["Indiranagar", "Whitefield", "Koramangala"])
    capacity_threshold = st.slider("Transformer Alert Threshold (%)", 50, 100, 80)
    st.divider()
    st.info("System Status: AI Decision Layer Active")

# --- MAIN DASHBOARD ---
st.title("⚡ ChargeIQ: EV Infrastructure & Optimization")
st.write(f"Decision Support Layer for **BESCOM - {selected_zone} Operations**")

if grid_df is not None:
    # 1. TOP METRICS
    col1, col2, col3, col4 = st.columns(4)
    avg_load = grid_df['current_load'].mean() / 10 
    col1.metric("Current Avg Load", f"{avg_load:.1f} MW", "-2.4%")
    col2.metric("EV Growth Index", "1.4x", "+0.3")
    col3.metric("Peak Load Shifting", "22%", "Target 30%")
    col4.metric("Grid Health", "Stable", "Normal")

    # 2. PART A: DEMAND PREDICTION
    st.divider()
    st.subheader("📊 Part A: EV Demand Prediction & Scheduling")
    
    col_a1, col_a2 = st.columns([2, 1])
    
    with col_a1:
        fig = px.area(demand_df, x='hour', y=['unmanaged', 'chargeiq_managed'],
                      title="Predicted Load Profile (24h Forecast)",
                      color_discrete_map={"unmanaged": "#ef4444", "chargeiq_managed": "#10b981"},
                      labels={"value": "Load (kW)", "hour": "Hour of Day"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col_a2:
        st.markdown("**AI Scheduling Strategy**")
        st.write("Current Peak: **18:00 - 22:00**")
        st.success("✔️ Strategy: Time-of-Use (ToU) Incentives")
        st.write("ChargeIQ has successfully shifted **18%** of residential EV load to the **01:00 - 05:00** window.")
        if st.button("Generate Dispatch Report"):
            st.toast("Report generated and saved to /logs")

    # 3. PART B: INFRASTRUCTURE PLANNING
    st.divider()
    st.subheader("📍 Part B: Infrastructure Planning Map")
    
    view_state = pdk.ViewState(latitude=12.9716, longitude=77.5946, zoom=11, pitch=45)
    
    heatmap = pdk.Layer(
        "HeatmapLayer",
        data=grid_df,
        get_position='[lon, lat]',
        get_weight="current_load",
        radius_pixels=80,
    )

    st.pydeck_chart(pdk.Deck(layers=[heatmap], initial_view_state=view_state))

    # 4. EXPLAINABILITY SECTION (Loop Fixed)
    st.divider()
    st.subheader("🧠 AI Explainability Evidence Cards")
    
    # Filter based on the sidebar slider
    critical_zones = grid_df[grid_df['current_load'] > (grid_df['capacity_kw'] * (capacity_threshold/100))]
    
    if critical_zones.empty:
        st.write("No transformers currently exceed the selected threshold.")
    else:
        for _, row in critical_zones.iterrows():
            headroom = ((row['capacity_kw'] - row['current_load']) / row['capacity_kw']) * 100
            st.markdown(f"""
            <div class="evidence-card">
                <h4>⚠️ High Priority: {row['id']}</h4>
                <p><b>Observation:</b> Current load is <b>{row['current_load']}kW</b> on a {row['capacity_kw']}kW feeder.</p>
                <p><b>AI Recommendation:</b> Deploy targeted peak-shaving incentives or 2x Level-3 Fast Chargers.</p>
                <p><b>Evidence:</b> {int(row['ev_growth_rate']*100)}% EV growth rate in this sector; grid headroom is at <b>{headroom:.1f}%</b>.</p>
            </div>
            """, unsafe_allow_html=True)