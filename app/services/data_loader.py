import pandas as pd
from config import DATA_DIR
from app.data import analytic, datasets, tickets, incidents
from app.data.db import connect_database

# ---------- CSV Loading ----------
def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    if not csv_path.exists():
        print(f"🔺 CSV file not found: {csv_path}")
        return 0

    try:
        df = pd.read_csv(csv_path)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        print(f"✅ Loaded {len(df)} rows into '{table_name}'")
        return len(df)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return 0

def load_all_csv_data(conn):
    """
    Load all CSV datasets into the database.
    Returns total number of rows loaded.
    """
    total = 0
    total += load_csv_to_table(conn, DATA_DIR / "cyber_incidents.csv", "cyber_incidents")
    total += load_csv_to_table(conn, DATA_DIR / "datasets_metadata.csv", "datasets_metadata")
    total += load_csv_to_table(conn, DATA_DIR / "it_tickets.csv", "it_tickets")
    return total

# ---------- Context Summarization ----------
def get_domain_context(domain: str) -> str:
    """
    Load domain-specific context from the database and return as a text summary.
    """
    conn = connect_database()

    if domain == "Cybersecurity":
        df_all = incidents.get_all_incidents(conn).head(5)
        df1 = analytic.get_incidents_by_category_count(conn)
        df2 = analytic.get_high_severity_by_status(conn)
        summary = (
            f"Recent incidents:\n{df_all.to_string(index=False)}\n\n"
            f"Incident categories:\n{df1.to_string(index=False)}\n\n"
            f"High severity by status:\n{df2.to_string(index=False)}"
        )

    elif domain == "Datasets":
        df_all = datasets.get_all_datasets(conn).head(5)
        df2 = analytic.get_datasets_by_uploader(conn)
        df3 = analytic.get_dataset_sizes(conn)
        summary = (
            f"Recent datasets:\n{df_all.to_string(index=False)}\n\n"
            f"Datasets by uploader:\n{df2.to_string(index=False)}\n\n"
            f"Dataset sizes:\n{df3.to_string(index=False)}"
        )

    elif domain == "Tickets":
        df_all = tickets.get_all_tickets(conn).head(5)
        df1 = analytic.get_tickets_by_status(conn)
        df2 = analytic.get_avg_resolution_time(conn)
        df3 = analytic.get_tickets_by_assignee(conn)
        summary = (
            f"Recent tickets:\n{df_all.to_string(index=False)}\n\n"
            f"Tickets by status:\n{df1.to_string(index=False)}\n\n"
            f"Avg resolution time:\n{df2.to_string(index=False)}\n\n"
            f"Tickets by assignee:\n{df3.to_string(index=False)}"
        )

    else:
        summary = "No domain-specific context available."

    conn.close()
    return summary