import streamlit as st
import json
import pandas as pd
from classifier import classify_po

# 1. Page Configuration
st.set_page_config(page_title="PO Category Classifier", layout="wide")

st.title("📦 PO L1–L2–L3 Classifier")
st.markdown("Enter the Purchase Order details below to identify the correct tax and spend categories.")

# 2. Create two columns for a better UI flow
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Input Details")
    po_description = st.text_area("PO Description", height=150, placeholder="e.g., Annual subscription for cloud hosting services...")
    supplier = st.text_input("Supplier (optional)", placeholder="e.g., Amazon Web Services")
    
    classify_btn = st.button("Classify PO", type="primary", use_container_width=True)

with col2:
    st.subheader("Classification Result")
    
    if classify_btn:
        if not po_description.strip():
            st.warning("Please enter a PO description.")
        else:
            with st.spinner("Analyzing taxonomy..."):
                # Call your existing logic
                result = classify_po(po_description, supplier)

            try:
                # Parse the result to ensure it's valid JSON
                parsed_result = json.loads(result)
                
                # Display the JSON nicely
                st.success("Analysis Complete!")
                st.json(parsed_result)

                # Add a Download Button so the user can save the result
                st.download_button(
                    label="Download Result as JSON",
                    data=json.dumps(parsed_result, indent=4),
                    file_name="po_classification.json",
                    mime="application/json",
                    use_container_width=True
                )
            except Exception:
                st.error("Model returned an unexpected format.")
                st.text(result)
    else:
        st.info("Results will appear here once you click 'Classify'.")

# 3. Simple Footer
st.divider()
st.caption("AI-powered Procurement Categorization Tool v1.1")
