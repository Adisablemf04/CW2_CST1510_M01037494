import streamlit as st
import pandas as pd
import datetime
from app.data.analytic import (
    get_incidents_by_category_count,
    get_high_severity_by_status,
    get_categories_with_many_cases
)
from app.data.db import connect_database

st.set_page_config(page_title="Incidents", page_icon="🚨", layout="wide")

# Ensure session state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, redirect
if not st.session_state.logged_in:
    st.error("You must be logged in to view incidents.")
    if st.button("Go to login page", width="stretch"):
        st.switch_page("Login.py")
    st.stop()

# Connect to DB
conn = connect_database()

# Page title
st.title("🚨 Incident Analytics")
st.success(f"Hello, **{st.session_state.username}**! Here’s your incident breakdown.")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    min_cases = st.slider("Minimum cases per category", 1, 20, 5)

# --- Add Incident Form ---
with st.expander("➕ Add Incident"):
    st.markdown("Fill out the form to report a new cybersecurity incident.")

    incident_date = st.date_input("Date of Incident", value=datetime.date.today())
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    category = st.selectbox("Category", ["Phishing", "Malware", "Data Breach", "Unauthorized Access", "Other"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    description = st.text_area("Description")
    reported_by = st.session_state.username or "admin"

    if st.button("Submit Incident", type="primary", width="stretch"):
        if description.strip() == "":
            st.warning("Please enter a description before submitting.")
        else:
            insert_query = """
                INSERT INTO cyber_incidents (timestamp, severity, category, status, description)
                VALUES (?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (incident_date.strftime("%Y-%m-%d"), severity, category, status, description))
            conn.commit()
            st.success("Incident submitted successfully!")
            st.toast("New incident added.")
            st.rerun()

# --- Summary Metrics ---
incident_query = """
    SELECT incident_id, timestamp, severity, category, status, description
    FROM cyber_incidents
"""
incident_df = pd.read_sql_query(incident_query, conn)

total_incidents = len(incident_df)
high_critical = incident_df[incident_df["severity"].isin(["High", "Critical"])].shape[0]
open_incidents = incident_df[incident_df["status"] == "Open"].shape[0]

st.markdown("### 📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🗂️ Total Incidents", total_incidents)
col2.metric("🔥 High/Critical", high_critical)
col3.metric("🚩 Open Incidents", open_incidents)

# --- Incident Records Table (with search + export) ---
st.markdown("### 📑 Incident Records")
if not incident_df.empty:
    incident_df = incident_df.rename(columns={
        "incident_id": "ID",
        "timestamp": "Date",
        "severity": "Severity",
        "category": "Category",
        "status": "Status",
        "description": "Description"
    })

    # Search box
    search_term = st.text_input("🔍 Search incidents", "")
    filtered_df = incident_df[
        incident_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
    ] if search_term else incident_df

    # Display table
    st.dataframe(filtered_df, width="stretch")

    # Export to CSV
    st.download_button(
        label="📥 Export filtered incidents to CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_incidents.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No incident records available.")

# --- Incidents by Category ---
st.subheader("📊 Incidents by Category")
incidents_df = get_incidents_by_category_count(conn)
if not incidents_df.empty:
    st.bar_chart(incidents_df.set_index("category"))
    with st.expander("See raw incident data"):
        st.dataframe(incidents_df, width="stretch")
else:
    st.info("No incident data available.")

# --- High Severity by Status ---
st.subheader("🔥 High Severity Incidents by Status")
high_sev_df = get_high_severity_by_status(conn)
if not high_sev_df.empty:
    st.bar_chart(high_sev_df.set_index("status"))
    with st.expander("See raw high severity data"):
        st.dataframe(high_sev_df, width="stretch")
else:
    st.info("No high severity data available.")

# --- Categories with Many Cases ---
st.subheader(f"📈 Categories with More Than {min_cases} Cases")
many_cases_df = get_categories_with_many_cases(conn, min_cases)
if not many_cases_df.empty:
    st.bar_chart(many_cases_df.set_index("category"))
    with st.expander("See raw filtered categories"):
        st.dataframe(many_cases_df, width="stretch")
else:
    st.info("No categories meet the threshold.")

# Logout button
st.divider()
if st.button("Log out", width="stretch"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Login.py")