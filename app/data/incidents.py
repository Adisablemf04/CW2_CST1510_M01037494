import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, incident_id, timestamp, severity, category, status, description):
    """
    Insert a new cyber incident into the database.

    Args:
        conn: Database connection
        incident_id: Unique ID of the incident
        timestamp: Date/time of the incident (YYYY-MM-DD HH:MM:SS)
        severity: Severity level (e.g., Low, Medium, High, Critical)
        category: Incident category (e.g., Malware, Phishing, DDoS)
        status: Current status (e.g., Open, Resolved, Closed)
        description: Incident description

    Returns:
        int: ID of the inserted incident (incident_id)
    """
    cursor = conn.cursor()

    query = """
        INSERT INTO cyber_incidents (
            incident_id, timestamp, severity, category, status, description
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (incident_id, timestamp, severity, category, status, description))
    conn.commit()

    return incident_id  # since incident_id is the primary key

def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.

    Args:
        conn: Database connection

    Returns:
        pandas.DataFrame: All incidents
    """
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY incident_id DESC", conn)
    return df

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.

    Args:
        conn: Database connection
        incident_id: ID of the incident to update
        new_status: New status value (e.g., 'Resolved', 'Open', 'Closed')

    Returns:
        int: Number of rows updated
    """
    cursor = conn.cursor()

    query = "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?"
    cursor.execute(query, (new_status, incident_id))
    conn.commit()

    return cursor.rowcount

def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.

    Args:
        conn: Database connection
        incident_id: ID of the incident to delete

    Returns:
        int: Number of rows deleted
    """
    cursor = conn.cursor()

    query = "DELETE FROM cyber_incidents WHERE incident_id = ?"
    cursor.execute(query, (incident_id,))
    conn.commit()

    return cursor.rowcount