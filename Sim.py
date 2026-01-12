
"""
Streamlined Prepaid SIM Activation System (Streamlit App)

This Streamlit application simulates a streamlined prepaid SIM activation
workflow aimed at reducing Average Handling Time (AHT).

Key Features:
- Individual customer verification via form input
- Bulk customer verification via CSV upload or Google Drive CSV
- Automated AHT tracking and comparison with traditional methods
- Interactive AHT dashboard using Plotly visualizations

The app demonstrates how automation, structured data intake,
and batch processing can significantly reduce operational handling time.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import time
import requests
import os
from io import StringIO


def convert_drive_url_to_csv_download(url: str) -> str:
    if "docs.google.com/spreadsheets" in url:
        sheet_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return url

@st.cache_data(show_spinner=False)
def load_csv_from_google_drive(url: str) -> pd.DataFrame:
    direct_url = convert_drive_url_to_csv_download(url)

    try:
        response = requests.get(direct_url, timeout=30)
        response.raise_for_status()

        # Guard: Google Drive returning HTML instead of CSV
        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            raise ValueError("Google Drive returned HTML instead of CSV")
        from io import StringIO

        df = pd.read_csv(StringIO(response.text))


        if df.empty:
            raise ValueError("CSV is empty")

        return df

    except Exception as e:
        st.error(f"❌ Failed to load CSV from Google Drive: {e}")
        st.stop()
GOOGLE_CSV_URL = "https://docs.google.com/spreadsheets/d/1uE3fuUJl1NR3C0LvkEdDWb-h14ouX3xLCuJaEo59ZKQ/edit?usp=sharing"
# Initialize session state for tracking AHTs
if 'streamlined_ahts' not in st.session_state:
    st.session_state.streamlined_ahts = []

# Sample traditional AHT data (simulating longer handling times)
traditional_ahts = [120, 150, 130, 140, 110]  # in seconds

st.title("Jimmy's Streamlined Prepaid SIM Activation System")
st.markdown("""
This system streamlines customer verification for prepaid SIM activation to reduce Average Handling Time (AHT).
It provides a simple form for individual input, automated verification simulation, and now supports bulk upload for companies.
The dashboard compares traditional vs. streamlined AHT.
""")

# Tabs for individual and bulk upload
tab1, tab2 = st.tabs(["Individual Verification", "Bulk Upload for Companies"])

with tab1:
    # Verification Form for individual
    with st.form("Customer Verification Form"):
        name = st.text_input("Customer Name")
        id_number = st.text_input("ID Number")
        address = st.text_area("Address")
        phone_number = st.text_input("Phone Number")
        reg_date = st.date_input("Registration Date")
        submit = st.form_submit_button("Verify and Activate")

    if submit:
        if name and id_number and address and phone_number:
            start_time = time.time()
            # Simulate streamlined verification process (quick checks)
            time.sleep(0.5)  # Reduced time for streamlined process
            end_time = time.time()
            aht = end_time - start_time
            st.session_state.streamlined_ahts.append(aht)
            st.success(f"Verification successful! SIM activated for {name}. AHT: {aht:.2f} seconds.")
        else:
            st.error("Please fill in all fields.")

with tab2:
    st.markdown("""
    ### Bulk Upload Instructions
    Required columns: - name- id_number- id_number- address- phone_number - reg_date
    """)

    st.subheader("📂 Data Source")

    source = st.radio(
        "Choose data source",
        ["Use Google Drive CSV", "Upload CSV Manually"]
    )

    df = None

    # OPTION 1: GOOGLE DRIVE CSV
    if source == "Use Google Drive CSV":
        st.info("Loading CSV from Google Drive...")
        df = load_csv_from_google_drive(GOOGLE_CSV_URL)
        st.success("CSV loaded successfully from Google Drive")

    # OPTION 2: MANUAL UPLOAD
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded successfully")


    # PROCESS CSV (COMMON LOGIC)
    if df is not None:
        required_columns = ["name", "id_number", "address", "phone_number", "reg_date"]

        if not all(col in df.columns for col in required_columns):
            st.error(f"Missing required columns: {', '.join(required_columns)}")
            st.stop()

        st.success(f"Processing {len(df)} records...")
        batch_ahts = []

        for index, row in df.iterrows():
            if row[required_columns].isna().any():
                st.warning(f"Skipping row {index + 1}: Missing data")
                continue

            start_time = time.time()
            time.sleep(0.5)  # Simulated streamlined verification
            aht = time.time() - start_time

            batch_ahts.append(aht)
            st.write(f"✅ Verified: {row['name']} — AHT: {aht:.2f}s")

        st.session_state.streamlined_ahts.extend(batch_ahts)
        st.success(f"Batch complete: {len(batch_ahts)} verifications")


# AHT Dashboard
st.header("AHT Dashboard")

if st.session_state.streamlined_ahts:
    avg_streamlined = sum(st.session_state.streamlined_ahts) / len(st.session_state.streamlined_ahts)
else:
    avg_streamlined = 0

avg_traditional = sum(traditional_ahts) / len(traditional_ahts) if traditional_ahts else 0

# Prepare data for visualization
data = pd.DataFrame({
    "Method": ["Traditional", "Streamlined"],
    "Average AHT (seconds)": [avg_traditional, avg_streamlined]
})

# Bar chart for AHT comparison
fig_bar = px.bar(data, x="Method", y="Average AHT (seconds)", title="AHT Comparison: Traditional vs. Streamlined",
                 color="Method", text="Average AHT (seconds)")
fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_bar)

# Line chart for streamlined AHT over activations
if st.session_state.streamlined_ahts:
    streamlined_df = pd.DataFrame({
        "Activation Number": list(range(1, len(st.session_state.streamlined_ahts) + 1)),
        "AHT (seconds)": st.session_state.streamlined_ahts
    })
    fig_line = px.line(streamlined_df, x="Activation Number", y="AHT (seconds)",
                       title="Streamlined AHT Over Multiple Activations")
    st.plotly_chart(fig_line)

st.markdown("""
### How This Reduces AHT:
- **Streamlined Process**: Minimal fields, instant submission, and simulated quick verification reduce manual steps.
- **Bulk Upload**: Allows companies to upload multiple entries at once for faster processing.
- **Traditional Simulation**: Assumes higher AHT based on sample data (e.g., manual checks, more fields).
- Perform verifications (individual or bulk) to see the average AHT update in real-time.

""")
