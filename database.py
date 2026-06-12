import sqlite3
from datetime import datetime

# ---------------------------------
# INITIALIZATION FUNCTION
# ---------------------------------
def init_db():
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # PREDICTION HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        disease TEXT,
        prediction TEXT,
        risk_score INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database Initialized/Created Successfully")

# ---------------------------------
# HELPER DB FUNCTIONS
# ---------------------------------
def save_prediction(username, disease, prediction, risk_score):
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()
    
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO prediction_history (username, disease, prediction, risk_score, date)
    VALUES (?, ?, ?, ?, ?)
    """, (username, disease, prediction, int(risk_score), date_str))
    
    conn.commit()
    conn.close()

def get_prediction_history(username):
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT disease, prediction, risk_score, date
    FROM prediction_history
    WHERE username = ?
    ORDER BY date DESC
    """, (username,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()

