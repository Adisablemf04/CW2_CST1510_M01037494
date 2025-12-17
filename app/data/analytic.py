import pandas as pd

def get_incidents_by_category_count(conn):
    """
    Count incidents by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY

    Returns:
        pandas.DataFrame: Incident category counts
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY

    Returns:
        pandas.DataFrame: High severity counts by status
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_categories_with_many_cases(conn, min_count=5):
    """
    Find incident categories with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY

    Args:
        conn: Database connection
        min_count: Minimum number of cases to include

    Returns:
        pandas.DataFrame: Categories with many cases
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

def get_datasets_by_uploader(conn):
    """
    Count datasets grouped by uploader.
    Uses: SELECT, FROM, GROUP BY, ORDER BY

    Returns:
        pandas.DataFrame: Dataset counts by uploader
    """
    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_dataset_sizes(conn):
    """
    Show rows and columns for each dataset.
    Uses: SELECT, FROM, ORDER BY

    Returns:
        pandas.DataFrame: Dataset sizes (rows, columns)
    """
    query = """
    SELECT name, rows, columns
    FROM datasets_metadata
    ORDER BY rows DESC
    """
    return pd.read_sql_query(query, conn)

def get_tickets_by_status(conn):
    """
    Count tickets grouped by status.
    Uses: SELECT, FROM, GROUP BY, ORDER BY

    Returns:
        pandas.DataFrame: Ticket counts by status
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_avg_resolution_time(conn):
    """
    Calculate average resolution time for tickets.
    Uses: SELECT, FROM, AVG

    Returns:
        pandas.DataFrame: Average resolution time (hours)
    """
    query = "SELECT AVG(resolution_time_hours) as avg_resolution FROM it_tickets"
    return pd.read_sql_query(query, conn)

def get_tickets_by_assignee(conn):
    """
    Count tickets grouped by assigned staff.
    Uses: SELECT, FROM, GROUP BY, ORDER BY

    Returns:
        pandas.DataFrame: Ticket counts by assignee
    """
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)