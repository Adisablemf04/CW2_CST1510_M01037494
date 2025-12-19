CST1510 Coursework 2 – Multi-Domain Intelligence Platform
Pawan Goness - M01037494
Degree: BSc Computer Science (Systems Engineering)

Project Overview
A secure, real-time web application built with Python + Streamlit that delivers intelligent insights for three domains:

Cybersecurity Analysts – track and respond to incidents
Data Scientists – manage and visualize dataset metadata
IT Administrators – monitor and prioritize support tickets
Operations domains are implemented with dedicated views and visualizations.

Key Features
Secure Authentication – bcrypt hashing, login/registration with SQLite backend (Week 7)
Database Persistence – SQLite with real data loaded from 3 CSV files (Week 8)
Live Cybersecurity Dashboard – metrics, interactive bar chart, real-time table (Week 9)
Incident Reporting – form to add new incidents with instant update
Multi-Domain Navigation – sidebar switching between Cybersecurity, Data Science, and IT Operations
Gemini AI Assistant – sidebar AI that analyzes current incidents using real data (Week 10)
Professional UI – dark mode, responsive layout, clean design

Instruction
Create a file at:
.streamlit/secrets.toml
Inside that file, add:
GEMINI_API_KEY = "your-api-key-here"
Replace with your actual Gemini API key.

How to Run Locally
# Clone the repository
git clone https://github.com/Adisablemf04/CW2_CST1510_M01037494.git

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Login.py