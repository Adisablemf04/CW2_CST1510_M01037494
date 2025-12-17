import streamlit as st
import pandas as pd
import datetime
from app.data.analytic import (
    get_tickets_by_status,
    get_tickets_by_assignee,
    get_avg_resolution_time
)
from app.data.db import connect_database

st.set_page_config(page_title="Tickets", page_icon="🎟️", layout="wide")

# Ensure session state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, redirect
if not st.session_state.logged_in:
    st.error("You must be logged in to view tickets.")
    if st.button("Go to login page", width="stretch"):
        st.switch_page("Login.py")
    st.stop()

# Connect to DB
conn = connect_database()

# Page title
st.title("🎟️ Ticket Analytics")
st.success(f"Hello, **{st.session_state.username}**! Here’s your ticket breakdown.")

# --- Add Ticket Form ---
with st.expander("➕ Add Ticket"):
    st.markdown("Fill out the form to create a new IT ticket.")

    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    assigned_to = st.text_input("Assigned To")
    created_at = st.date_input("Created At", value=datetime.date.today())
    resolution_time_hours = st.number_input("Resolution Time (hours)", min_value=0.0, step=0.5)

    if st.button("Submit Ticket", type="primary", width="stretch"):
        if description.strip() == "":
            st.warning("Please enter a description before submitting.")
        else:
            insert_query = """
                INSERT INTO it_tickets (priority, description, status, assigned_to, created_at, resolution_time_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            conn.execute(insert_query, (
                priority,
                description,
                status,
                assigned_to,
                created_at.strftime("%Y-%m-%d"),
                resolution_time_hours
            ))
            conn.commit()
            st.success("Ticket submitted successfully!")
            st.toast("New ticket added.")
            st.rerun()

# --- Summary Metrics ---
ticket_query = """
    SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
    FROM it_tickets
"""
ticket_df = pd.read_sql_query(ticket_query, conn)

total_tickets = len(ticket_df)
open_tickets = ticket_df[ticket_df["status"] == "Open"].shape[0]
avg_resolution = ticket_df["resolution_time_hours"].mean() if not ticket_df.empty else 0

st.markdown("### 📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🎫 Total Tickets", total_tickets)
col2.metric("📬 Open Tickets", open_tickets)
col3.metric("⏱️ Avg Resolution (hrs)", round(avg_resolution, 2))

# --- Ticket Records Table (with search + export) ---
st.markdown("### 📑 Ticket Records")
if not ticket_df.empty:
    ticket_df = ticket_df.rename(columns={
        "ticket_id": "ID",
        "priority": "Priority",
        "description": "Description",
        "status": "Status",
        "assigned_to": "Assigned To",
        "created_at": "Created At",
        "resolution_time_hours": "Resolution Time (hrs)"
    })

    # Search box
    search_term = st.text_input("🔍 Search tickets", "")
    filtered_df = ticket_df[
        ticket_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
    ] if search_term else ticket_df

    # Display table
    st.dataframe(filtered_df, width="stretch")

    # Export to CSV
    st.download_button(
        label="📥 Export filtered tickets to CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_tickets.csv",
        mime="text/csv",
        width="stretch"
    )
else:
    st.info("No ticket records available.")

# --- Tickets by Status ---
st.subheader("📊 Tickets by Status")
tickets_df = get_tickets_by_status(conn)
if not tickets_df.empty:
    st.bar_chart(tickets_df.set_index("status"))
    with st.expander("See raw ticket data"):
        st.dataframe(tickets_df, width="stretch")
else:
    st.info("No ticket data available.")

# --- Tickets by Assignee ---
st.subheader("👤 Tickets by Assignee")
assignee_df = get_tickets_by_assignee(conn)
if not assignee_df.empty:
    st.bar_chart(assignee_df.set_index("assigned_to"))
    with st.expander("See raw assignee data"):
        st.dataframe(assignee_df, width="stretch")
else:
    st.info("No assignee data available.")

# --- Average Resolution Time ---
st.subheader("⏱️ Average Resolution Time")
avg_res_df = get_avg_resolution_time(conn)
if not avg_res_df.empty:
    avg_hours = avg_res_df["avg_resolution"].iloc[0]
    st.metric("Avg Resolution Time (hours)", f"{avg_hours:.2f}")
else:
    st.info("No resolution time data available.")

# Logout button
st.divider()
if st.button("Log out", width="stretch"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Login.py")