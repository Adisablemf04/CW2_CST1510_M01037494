import pandas as pd

def get_incidents_by_type_count(conn):
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