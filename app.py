import streamlit as st
import json
import time
from classifier import classify_po

# 1. Page Config with an Emoji Icon
st.set_page_config(page_title="AI Procurement Engine", layout="wide", initial_sidebar_state="expanded")

# 2. Custom CSS for "Wow" Styling
st.markdown("""
    <style>
    /* Main background and font */
    .stApp {
        background-color: #0e1117;
    }
    /* Custom Card Styling for results */
    .category-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 10px;
    }
    /* Title Gradient */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar with Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("## AI Engine v2.0")
    st.write("Precision classification for modern procurement.")
    st.divider()
    accent_color = st.color_picker("UI Accent Color", "#3b82f6")

# 4. Header Section
st.markdown('<h1 class="main-title">Procurement AI Explorer</h1>', unsafe_allow_html=True)
st.write("Automated L1–L3 Taxonomy Mapping")

# 5. Main Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📝 Input Specification")
    with st.container():
        po_description = st.text_area("PO Description", height=180, placeholder="Paste description here...")
        supplier = st.text_input("📍 Supplier Name (Optional)")
        
        # Big high-action button
        if st.button("RUN AI CLASSIFICATION", type="primary", use_container_width=True):
            if not po_description.strip():
                st.error("Missing input data.")
            else:
                # Execution Logic
                with st.spinner("🧠 Neural Network Processing..."):
                    time.sleep(1.5) # Forced delay for "Wow" effect
                    result = classify_po(po_description, supplier)
                st.session_state['result'] = result
                st.session_state['processed'] = True

with col2:
    st.subheader("🎯 Classification Output")
    
    if st.session_state.get('processed'):
        try:
            data = json.loads(st.session_state['result'])
            
            # Dynamic Results Display using custom HTML/CSS
            st.markdown(f"""
                <div class="category-card">
                    <small style="color: #9ca3af;">L1 DOMAIN</small>
                    <h2 style="margin:0; color: white;">{data.get('L1', 'Unclassified')}</h2>
                </div>
                <div class="category-card" style="border-left-color: #10b981;">
                    <small style="color: #9ca3af;">L2 CATEGORY</small>
                    <h3 style="margin:0; color: white;">{data.get('L2', 'Unclassified')}</h3>
                </div>
                <div class="category-card" style="border-left-color: #f59e0b;">
                    <small style="color: #9ca3af;">L3 SUB-GROUP</small>
                    <h4 style="margin:0; color: white;">{data.get('L3', 'Unclassified')}</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons in a Row
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.download_button("📩 Export JSON", json.dumps(data), file_name="output.json", use_container_width=True)
            with btn_col2:
                if st.button("🔄 Clear", use_container_width=True):
                    st.session_state['processed'] = False
                    st.rerun()

        except Exception:
            st.error("Data Parsing Error")
            st.code(st.session_state['result'])
    else:
        # Professional Empty State
        st.info("Upload or type a PO description to begin neural mapping.")
        st.image("https://cdn.dribbble.com/users/148670/screenshots/4518301/empty_state.png", use_container_width=True)

st.divider()
