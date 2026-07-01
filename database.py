import sqlite3

# =====================================================
# CONNECT DATABASE
# =====================================================

conn = sqlite3.connect("health_app.db")

# =====================================================
# CREATE CURSOR
# =====================================================

cursor = conn.cursor()

# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_records (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT,

    dob TEXT,

    email TEXT,

    glucose REAL,

    haemoglobin REAL,

    cholesterol REAL,

    prediction TEXT
)
""")

# =====================================================
# SAVE CHANGES
# =====================================================

conn.commit()

# =====================================================
# CLOSE CONNECTION
# =====================================================

conn.close()

print("Database and table created successfully.")

