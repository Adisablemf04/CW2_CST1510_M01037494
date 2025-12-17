import pandas as pd

def insert_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """Insert a new IT ticket."""
    cursor = conn.cursor()
    query = """
        INSERT INTO it_tickets (
            ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit()
    return ticket_id

def get_all_tickets(conn):
    """Retrieve all IT tickets."""
    return pd.read_sql_query("SELECT * FROM it_tickets ORDER BY created_at DESC", conn)

def update_ticket_status(conn, ticket_id, new_status):
    """Update the status of a ticket."""
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """Delete a ticket."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount