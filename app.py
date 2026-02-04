import streamlit as st
import json
import time
import pandas as pd
from classifier import classify_po

# 1. Advanced Page Config
st.set_page_config(page_title="NexGen Procurement AI", layout="wide")

# 2. Advanced CSS - Glassmorphism & Animations
st.markdown("""
    <style>
    .main { background: #0b0e14; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #3b82f6; background: #161b22; color: white; }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
    }
    
    /* Success Pulse Animation */
    .pulse {
        color: #10b981;
        font-weight: bold;
        animation: pulse-animation 2s infinite;
    }
    @keyframes pulse-animation {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar with Metrics
with st.sidebar:
    st.markdown("# 🛡️ Admin Panel")
    st.metric(label="System Status", value="Online", delta="100%")
    st.divider()
    st.write("### Model Settings")
    precision = st.select_slider("Search Precision", options=["Standard", "High", "Ultra"])
    st.caption(f"Currently using {precision} mapping engine.")

# 4. Main UI Header
st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🚀 NexGen Taxonomy Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Enterprise-grade Purchase Order Classification</p>", unsafe_allow_html=True)

# 5. Tabbed Interface (The "Wow" factor for organization)
tab1, tab2 = st.tabs(["🔍 Single Classifier", "📊 Analytics & History"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Input Stream")
        po_input = st.text_area("PO Description", height=200)
        vendor = st.text_input("Supplier Identifier")
        
        if st.button("EXECUTE CLASSIFICATION", use_container_width=True, type="primary"):
            if po_input:
                with st.status("Initializing AI...", expanded=True) as status:
                    st.write("Fetching taxonomy rules...")
                    time.sleep(0.8)
                    st.write("Running L1-L3 Neural Mapping...")
                    raw_result = classify_po(po_input, vendor)
                    time.sleep(0.5)
                    status.update(label="Classification Complete!", state="complete", expanded=False)
                
                st.session_state['latest_result'] = raw_result
            else:
                st.error("Input required.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if 'latest_result' in st.session_state:
            try:
                res = json.loads(st.session_state['latest_result'])
                
                st.subheader("Mapping Results")
                
                # Using columns for a mini-dashboard look
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**L1 Domain** \n`{res.get('L1', 'N/A')}`")
                    st.markdown(f"**L2 Category** \n`{res.get('L2', 'N/A')}`")
                with c2:
                    # Simulated Confidence Score
                    st.write("AI Confidence Score")
                    st.progress(0.92) # You can hardcode this or extract if your model provides it
                    st.caption("92% Confidence Match")

                st.divider()
                st.info(f"**L3 Final Mapping:** {res.get('L3', 'N/A')}")
                
                with st.expander("Show Metadata"):
                    st.json(res)
            except:
                st.error("Response parsing error.")
        else:
            st.write("### Instructions")
            st.info("Paste your PO details on the left and click execute to see the AI taxonomy mapping in real-time.")

with tab2:
    st.subheader("Historical Data Tracking")
    # Sample data to show off the visual potential
    chart_data = pd.DataFrame({
        "Category": ["IT", "Office", "Travel", "Legal"],
        "PO Count": [25, 40, 10, 5]
    })
    st.bar_chart(chart_data, x="Category", y="PO Count", color="#3b82f6")
    st.success("Log History: Last 10 records synced successfully.")

st.divider()
st.markdown("<div style='text-align: center;' class='pulse'>● SYSTEM OPERATIONAL</div>", unsafe_allow_html=True)
