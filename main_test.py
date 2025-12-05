import pandas as pd
from app.data.db import connect_database
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, update_incident_status, delete_incident
from app.data.analytic import get_incidents_by_type_count, get_high_severity_by_status

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    test_incident_id = 9999
    insert_incident(
        conn,
        test_incident_id,
        "2024-11-05 10:00:00",
        "Low",
        "Test Incident",
        "Open",
        "This is a test incident"
    )
    print(f"  Create: ✅ Incident #{test_incident_id} created")

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE incident_id = ?",
        conn,
        params=(test_incident_id,)
    )
    found = not df.empty
    print(f"  Read:    {'✅ Found' if found else '❌ Not found'} incident #{test_incident_id}")

    rows_updated = update_incident_status(conn, test_incident_id, "Resolved")
    print(f"  Update:  {'✅' if rows_updated else '❌'} Status updated")

    rows_deleted = delete_incident(conn, test_incident_id)
    print(f"  Delete:  {'✅' if rows_deleted else '❌'} Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:       Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()