Student Name: Pawan Goness
Student ID: M01037494
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 character)

Week 8: Backend Testing & Verification

Objective:
To verify the functionality, integrity, and security of the backend database system before integrating a frontend interface in Week 9.

Testing & Verification Summary:
- Database connects successfully 
- All 4 tables created 
- Users migrated from users.txt 
- CSV data loaded 
- Registration works 
- Login works 
- Can create new incidents 
- Can read/query incidents 
- Can update incident status 
- Can delete incidents 
- Analytical queries return results 
- No SQL injection vulnerabilities (all queries use ? placeholders) 

Key Files Updated:
- main.py — Demo script for database setup, user migration, and CRUD testing
- main_test.py — Comprehensive test runner for authentication, CRUD, and analytics
- incidents.py — Updated insert_incident() to match new schema
- analytic.py — Fixed queries to use category instead of deprecated incident_type
- Requirements.txt — Cleaned to include only used packages: pandas, bcrypt==4.2.0

Notes:
- All test cases passed successfully
- Database is now fully aligned with CSV structure
- Ready for Week 9 Streamlit integration (login page, dashboard, forms, charts)