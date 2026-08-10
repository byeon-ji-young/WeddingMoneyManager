from .connection import get_connection

# ==========================================
# settings table
# ==========================================

# ==========================================
# READ
# ==========================================
def get_setting(key):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT value
            FROM settings
            WHERE key = ?
        """, (key,))

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    finally:
        conn.close()

# ==========================================
# CREATE / UPDATE
# ==========================================
def update_setting(key, value):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO settings(key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
        """, (
            key,
            str(value)
        ))

        conn.commit()

    finally:
        conn.close()