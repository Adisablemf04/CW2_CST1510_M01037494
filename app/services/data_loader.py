import pandas as pd
from config import DATA_DIR  # or from app.data.paths if needed

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
        print(f" Loaded {len(df)} rows into '{table_name}'")
        return len(df)
    except Exception as e:
        print(f" Error loading CSV: {e}")
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