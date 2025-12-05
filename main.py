from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)

    # 2. Migrate users
    migrate_users_from_file(conn)

    # 2b. Verify migration
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")
    print(f"\nTotal users: {len(users)}")

    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 4. Test CRUD (insert incident with new schema)
    incident_id = insert_incident(
        conn,
        2000,  # incident_id
        "2024-11-05 10:00:00",  # timestamp
        "High",  # severity
        "Phishing",  # category
        "Open",  # status
        "Suspicious email detected"  # description
    )
    print(f"Created incident #{incident_id}")

    # 5. Query data
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    conn.close()

if __name__ == "__main__":
    main()