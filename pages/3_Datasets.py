import streamlit as st
import pandas as pd
import datetime
from app.data.analytic import (
    get_datasets_by_uploader,
    get_dataset_sizes
)
from app.data.db import connect_database

st.set_page_config(page_title="Datasets", page_icon="📂", layout="wide")

# Ensure session state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, redirect
if not st.session_state.logged_in:
    st.error("You must be logged in to view datasets.")
    if st.button("Go to login page", width="stretch"):
        st.switch_page("Login.py")
    st.stop()

# Connect to DB
conn = connect_database()

# Page title
st.title("📂 Dataset Analytics")
st.success(f"Hello, **{st.session_state.username}**! Here’s your dataset breakdown.")

# --- Add Dataset Form ---
with st.expander("➕ Add Dataset"):
    st.markdown("Fill out the form to add a new dataset.")

    dataset_name = st.text_input("Dataset Name")
    rows = st.number_input("Number of Rows", min_value=0, step=1)
    columns = st.number_input("Number of Columns", min_value=0, step=1)
    uploaded_by = st.session_state.username or "admin"
    upload_date = st.date_input("Upload Date", value=datetime.date.today())

    if st.button("Submit Dataset", type="primary", width="stretch"):
        if dataset_name.strip() == "":
            st.warning("Please enter a dataset name before submitting.")
        else:
            insert_query = """
                INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date)
                VALUES (?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (dataset_name, rows, columns, uploaded_by, upload_date.strftime("%Y-%m-%d")))
            conn.commit()
            st.success("Dataset submitted successfully!")
            st.toast("New dataset added.")
            st.rerun()

# --- Summary Metrics ---
dataset_query = """
    SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
    FROM datasets_metadata
"""
dataset_df = pd.read_sql_query(dataset_query, conn)

total_datasets = len(dataset_df)
largest_dataset = dataset_df["rows"].max() if not dataset_df.empty else 0
unique_uploaders = dataset_df["uploaded_by"].nunique() if not dataset_df.empty else 0

st.markdown("### 📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🗂️ Total Datasets", total_datasets)
col2.metric("📈 Largest Dataset (rows)", largest_dataset)
col3.metric("👤 Unique Uploaders", unique_uploaders)

# --- Dataset Records Table (with search + export) ---
st.markdown("### 📑 Dataset Records")
if not dataset_df.empty:
    dataset_df = dataset_df.rename(columns={
        "dataset_id": "ID",
        "name": "Name",
        "rows": "Rows",
        "columns": "Columns",
        "uploaded_by": "Uploaded By",
        "upload_date": "Upload Date"
    })

    # Search box
    search_term = st.text_input("🔍 Search datasets", "")
    filtered_df = dataset_df[
        dataset_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
    ] if search_term else dataset_df

    # Display table
    st.dataframe(filtered_df, width="stretch")

    # Export to CSV
    st.download_button(
        label="📥 Export filtered datasets to CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_datasets.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No dataset records available.")

# --- Datasets by Uploader ---
st.subheader("📊 Datasets by Uploader")
datasets_df = get_datasets_by_uploader(conn)
if not datasets_df.empty:
    st.bar_chart(datasets_df.set_index("uploaded_by"))
    with st.expander("See raw dataset data"):
        st.dataframe(datasets_df, width="stretch")
else:
    st.info("No dataset data available.")

# --- Dataset Sizes ---
st.subheader("📏 Dataset Sizes (Rows & Columns)")
sizes_df = get_dataset_sizes(conn)
if not sizes_df.empty:
    st.dataframe(sizes_df, width="stretch")

    st.download_button(
        label="📥 Export dataset sizes to CSV",
        data=sizes_df.to_csv(index=False).encode("utf-8"),
        file_name="dataset_sizes.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No dataset size information available.")

# Logout button
st.divider()
if st.button("Log out", width="stretch"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Login.py")