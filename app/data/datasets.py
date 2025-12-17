import pandas as pd

def insert_dataset(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    """Insert a new dataset metadata record."""
    cursor = conn.cursor()
    query = """
        INSERT INTO datasets_metadata (
            dataset_id, name, rows, columns, uploaded_by, upload_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    conn.commit()
    return dataset_id

def get_all_datasets(conn):
    """Retrieve all dataset metadata records."""
    return pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY dataset_id DESC", conn)

def delete_dataset(conn, dataset_id):
    """Delete a dataset metadata record."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount