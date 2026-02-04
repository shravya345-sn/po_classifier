import streamlit as st
import json
import time
from classifier import classify_po

# 1. Page Configuration
st.set_page_config(page_title="Enterprise PO Classifier", layout="wide")

# 2. Sidebar - Makes the app look like a real tool
with st.sidebar:
    st.header("Help & Instructions")
    st.info("""
    **How to use:**
    1. Enter the description from the Purchase Order.
    2. Add the Supplier name if available.
    3. Click 'Classify' to see the L1/L2/L3 mapping.
    """)
    if st.button("Reset App"):
        st.rerun()

st.title("📦 PO L1–L2–L3 Classifier")

# 3. Two-Column Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Input Details")
    po_description = st.text_area("PO Description", height=150, placeholder="Describe the items or services...")
    supplier = st.text_input("Supplier (optional)")
    
    classify_btn = st.button("Classify PO", type="primary", use_container_width=True)

with col2:
    st.subheader("Classification Result")
    
    if classify_btn:
        if not po_description.strip():
            st.warning("Please enter a PO description.")
        else:
            # Visual Modification: Progress bar for "AI Thinking"
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005) # Makes the UI feel reactive
                bar.progress(i + 1)
            
            with st.spinner("Finalizing taxonomy..."):
                result = classify_po(po_description, supplier)

            try:
                data = json.loads(result)
                
                # Modification: Metric Cards for quick reading
                m1, m2, m3 = st.columns(3)
                m1.metric("L1 Category", data.get("L1", "N/A"))
                m2.metric("L2 Category", data.get("L2", "N/A"))
                m3.metric("L3 Category", data.get("L3", "N/A"))
                
                st.divider()
                
                # Display full JSON
                with st.expander("View Full JSON Response"):
                    st.json(data)

                # Download Button
                st.download_button(
                    label="Export Classification",
                    data=json.dumps(data, indent=4),
                    file_name="po_data.json",
                    mime="application/json",
                    use_container_width=True
                )
                
            except Exception:
                st.error("Invalid response format.")
                st.text(result)
    else:
        # Visual placeholder when empty
        st.info("Awaiting input for classification...")

st.divider()
st.caption("Developed for Procurement Operations | Version 1.2")
