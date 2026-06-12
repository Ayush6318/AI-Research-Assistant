import sqlite3

conn = sqlite3.connect(
  "chat_history.db",
  check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    session_id TEXT,

    role TEXT,

    content TEXT

)
""")

conn.commit()

def save_message(
    session_id,
    role,
    content
):
    cursor.execute(
        """
        INSERT INTO messages
        (
            session_id,
            role,
            content
        )
        VALUES
        (?, ?, ?)
        """,
        (
            session_id,
            role,
            content
        )
    )

    conn.commit()

def get_messages(
    session_id
):

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id=?
        ORDER BY id DESC LIMIT 10
        """,
        (session_id,)
    )

    return cursor.fetchall()
