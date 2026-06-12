import sqlite3

# Register User
def register_user(
    username,
    password
):
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users
        (username,password)
        VALUES (?,?)
        """,
        (username,password)
    )
    conn.commit()
    conn.close()

# Login User
def login_user(
    username,
    password
):
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (username,password)
    )
    user = cursor.fetchone()
    conn.close()
    return user

# Check Existing User
def user_exists(
    username
):
    conn = sqlite3.connect(
        "database.db",
        check_same_thread=False
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


