import streamlit as st
import json
import pandas as pd
import time
import plotly.express as px
import os
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="SecureGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# Path to shared data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'dashboard_data.json')

def load_data():
    try:
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"threats": [], "stats": {"packets": 0}}

# -- HEADER --
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛡️ SecureGuard AI Command Center")
    st.markdown("Real-time Network Security Monitoring & Threat Detection")
with col2:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    status_container = st.empty()

# -- SIDEBAR --
with st.sidebar:
    st.header("System Status")
    st.success("● Agent Active")
    st.info("● Cloud Sync: SIMULATED")
    
    st.markdown("---")
    st.subheader("Configuration")
    sensitivity = st.select_slider("Detection Sensitivity", options=["Low", "Medium", "High"], value="Medium")
    auto_block = st.checkbox("Auto-Block Threats", value=True)
    
    st.markdown("---")
    if st.button("Clear Logs"):
        # Reset JSON file
        with open(DATA_PATH, 'w') as f:
            json.dump({"threats": [], "stats": {"packets": 0}}, f)
        st.toast("Logs cleared!")

# -- MAIN DASHBOARD LOOP --
placeholder = st.empty()

while True:
    data = load_data()
    
    with placeholder.container():
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        
        threat_count = len(data.get('threats', []))
        total_packets = data.get('stats', {}).get('packets', 0)
        
        # Calculate Threat Level
        if threat_count == 0:
            level = "SAFE"
            color = "off"
        elif threat_count < 5:
            level = "ELEVATED"
            color = "normal"
        else:
            level = "CRITICAL"
            color = "inverse"
            
        m1.metric("Threat Level", level, f"{threat_count} alerts", delta_color=color)
        m2.metric("Packets Analyzed", f"{total_packets:,}", "+124/s")
        m3.metric("Active Connections", "42", "-3")
        m4.metric("Cloud Latency", "24ms", "stable")
        
        # Charts & Tables
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Live Threat Timeline")
            if data['threats']:
                df = pd.DataFrame(data['threats'])
                if not df.empty:
                    # -- FIX: Extract nested packet details if top-level fields are missing --
                    if 'src_ip_hash' not in df.columns and 'packet' in df.columns:
                        df['src_ip_hash'] = df['packet'].apply(lambda x: x.get('src_ip_hash', 'unknown') if isinstance(x, dict) else 'unknown')
                    
                    # Ensure all required columns exist
                    required_cols = ['timestamp', 'type', 'src_ip_hash', 'severity']
                    for col in required_cols:
                        if col not in df.columns:
                             # Default severity to 0.5 if missing, others to 'unknown'
                            df[col] = 0.5 if col == 'severity' else 'unknown'

                    # Processing for Visualization
                    df['datetime'] = pd.to_datetime(df['timestamp'])
                    df['severity_score'] = pd.to_numeric(df['severity'], errors='coerce').fillna(0.5)
                    
                    # 1. VISUAL TIMELINE CHART
                    # Scatter plot: Time on X, Threat Type on Y, Color/Size by Severity
                    fig_timeline = px.scatter(
                        df, 
                        x='datetime', 
                        y='type', 
                        color='severity_score',
                        size='severity_score',
                        size_max=25,
                        hover_data=['src_ip_hash', 'timestamp'],
                        color_continuous_scale=['#3b82f6', '#f59e0b', '#ef4444'], # Blue -> Orange -> Red
                        range_color=[0.4, 1.0],
                        title=""
                    )
                    
                    fig_timeline.update_layout(
                        plot_bgcolor='rgba(0,0,0,0.2)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e2e8f0'),
                        xaxis=dict(showgrid=False, title='Time (UTC)', gridcolor='#334155'),
                        yaxis=dict(showgrid=True, title='', gridcolor='#334155'),
                        margin=dict(l=0, r=0, t=0, b=0),
                        height=350,
                        showlegend=False
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)

                    # 2. RAW DATA (Collapsible)
                    with st.expander("📝 View Detailed Threat Logs"):
                        display_df = df[required_cols].copy()
                        display_df['timestamp'] = df['datetime'].dt.strftime('%H:%M:%S')
                        st.dataframe(
                            display_df, 
                            use_container_width=True,
                            column_config={
                                "type": "Threat Type",
                                "src_ip_hash": "Source IP",
                                "severity": st.column_config.ProgressColumn(
                                    "Severity",
                                    format="%.2f",
                                    min_value=0,
                                    max_value=1,
                                ),
                            }
                        )
            else:
                st.info("No threats detected. System is secure.")
                
        with c2:
            st.subheader("Attack Distribution")
            if data['threats']:
                counts = pd.DataFrame(data['threats'])['type'].value_counts()
                fig = px.pie(values=counts.values, names=counts.index, hole=0.4)
                fig.update_layout(
                    background_color="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=250
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.text("Waiting for data...")

        # Terminal Feed Simulation
        st.subheader("Live Agent Feed")
        with st.container(height=200):
            if data['threats']:
                for threat in data['threats'][:10]:
                    t_type = threat.get('type', 'UNKNOWN').upper()
                    t_time = threat.get('timestamp', '')
                    t_src = threat.get('src_ip_hash', 'unknown')
                    
                    if threat.get('severity', 0) > 0.8:
                        icon = "🔴"
                        color = "red"
                    else:
                        icon = "⚠️"
                        color = "orange"
                        
                    st.markdown(f":{color}[{icon} **{t_type}** detected from **{t_src}** at {t_time}]")
            else:
                st.code("Listening for network traffic...", language="bash")

    time.sleep(1)
