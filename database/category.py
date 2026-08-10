from .connection import get_connection

import sqlite3

# ==========================================
# category table
# ==========================================

# ==========================================
# READ - 콤보박스용
# ==========================================
def get_category_list():
    return [
        row["name"]
        for row in get_all_categories()
    ]

# ==========================================
# READ ALL
# ==========================================
def get_all_categories():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM categories
            ORDER BY id
        """)

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1]
            }
            for row in rows
        ]

    finally:
        conn.close()

# ==========================================
# CREATE
# ==========================================
def add_category(name):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO categories(name)
            VALUES (?)
        """, (name,))

        conn.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None
    
    finally:
        conn.close()

# ==========================================
# UPDATE
# ==========================================
def update_category(category_id, name):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE categories
            SET name = ?
            WHERE id = ?
        """, (
            name,
            category_id
        ))

        conn.commit()

    finally:
        conn.close()

# ==========================================
# READ - 사용 중인 카테고리 검색
# ==========================================
def is_category_used(category_name):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM expenses
            WHERE category = ?
        """, (category_name,))

        count = cursor.fetchone()[0] # fetchone(): SQL 실행 결과에서 한 줄(row)을 가져오는 함수. SQLite의 조회 결과는 튜플(tuple) 형태로 반환. 즉, (1,0) 이 형태로 반환됨

        return count > 0

    finally:
        conn.close()

# ==========================================
# DELETE
# ==========================================
def delete_category(category_id):
    conn = get_connection()
    
    try:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM categories
            WHERE id = ?
        """, (category_id,))

        conn.commit()

    finally:
        conn.close()