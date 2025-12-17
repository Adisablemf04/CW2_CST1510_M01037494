import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.analytic import (
    get_incidents_by_category_count,
    get_datasets_by_uploader,
    get_tickets_by_status
)
from app.data.db import connect_database
import time

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Ensure session state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Login.py")
    st.stop()

# Logged-in view
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
st.toast("Dashboard loaded successfully!")

# Connect to DB
conn = connect_database()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    st.caption("Adjust filters to refine analytics.")
    min_cases = st.slider("Minimum incident cases", 1, 20, 5)

# --- Cyber Incidents Section ---
st.subheader("🚨 Cyber Incidents")

incident_table_query = """
    SELECT incident_id, timestamp, severity, category, status, description
    FROM cyber_incidents
    ORDER BY timestamp DESC
"""
incident_table_df = pd.read_sql_query(incident_table_query, conn)

total_incidents = len(incident_table_df)
high_critical = incident_table_df[incident_table_df["severity"].isin(["High", "Critical"])].shape[0]
open_incidents = incident_table_df[incident_table_df["status"] == "Open"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("🧮 Total Incidents", total_incidents)
col2.metric("🔥 High/Critical", high_critical)
col3.metric("📬 Open Incidents", open_incidents)

if not incident_table_df.empty:
    severity_counts = incident_table_df["severity"].value_counts().reset_index()
    severity_counts.columns = ["Severity", "Count"]
    fig = px.bar(severity_counts, x="Severity", y="Count", title="Severity Breakdown", color="Severity")
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Incident Records")
    incident_table_df = incident_table_df.rename(columns={
        "incident_id": "ID",
        "timestamp": "Date",
        "severity": "Severity",
        "category": "Category",
        "status": "Status",
        "description": "Description"
    })
    st.dataframe(incident_table_df, width="stretch")
else:
    st.info("No incident records available.")

st.markdown("---")

# --- Datasets Section ---
st.subheader("📂 Datasets")

datasets_query = """
    SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
    FROM datasets_metadata
    ORDER BY upload_date DESC
"""
datasets_df = pd.read_sql_query(datasets_query, conn)

total_datasets = len(datasets_df)
largest_dataset = datasets_df["rows"].max() if not datasets_df.empty else 0
unique_uploaders = datasets_df["uploaded_by"].nunique() if not datasets_df.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Datasets", total_datasets)
col2.metric("📈 Largest Dataset (rows)", largest_dataset)
col3.metric("👤 Unique Uploaders", unique_uploaders)

if not datasets_df.empty:
    uploader_counts = datasets_df["uploaded_by"].value_counts().reset_index()
    uploader_counts.columns = ["Uploader", "Count"]
    fig = px.bar(uploader_counts, x="Uploader", y="Count", title="Datasets by Uploader", color="Uploader")
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Dataset Records")
    datasets_df = datasets_df.rename(columns={
        "dataset_id": "ID",
        "name": "Name",
        "rows": "Rows",
        "columns": "Columns",
        "uploaded_by": "Uploaded By",
        "upload_date": "Upload Date"
    })
    st.dataframe(datasets_df, width="stretch")
else:
    st.info("No dataset records available.")

st.markdown("---")

# --- Tickets Section ---
st.subheader("🎟️ Tickets")

tickets_query = """
    SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
    FROM it_tickets
    ORDER BY created_at DESC
"""
tickets_df = pd.read_sql_query(tickets_query, conn)

total_tickets = len(tickets_df)
open_tickets = tickets_df[tickets_df["status"] == "Open"].shape[0]
avg_resolution = tickets_df["resolution_time_hours"].mean() if not tickets_df.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("🎫 Total Tickets", total_tickets)
col2.metric("📬 Open Tickets", open_tickets)
col3.metric("⏱️ Avg Resolution (hrs)", round(avg_resolution, 2))

if not tickets_df.empty:
    status_counts = tickets_df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.bar(status_counts, x="Status", y="Count", title="Ticket Status Breakdown", color="Status")
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Ticket Records")
    tickets_df = tickets_df.rename(columns={
        "ticket_id": "ID",
        "priority": "Priority",
        "description": "Description",
        "status": "Status",
        "assigned_to": "Assigned To",
        "created_at": "Created At",
        "resolution_time_hours": "Resolution Time (hrs)"
    })
    st.dataframe(tickets_df, width="stretch")
else:
    st.info("No ticket records available.")

# Logout button
st.divider()
if st.button("Log out", width="stretch"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Login.py")