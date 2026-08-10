from .connection import get_connection # .: 현재 패키지 안에서 찾는다는 뜻
# 즉, 내가 있는 database 폴더 안의 connection.py에서 get_connection 가져오라는 뜻

# ==========================================
# expenses table
# ==========================================

# ==========================================
# CREATE
# ==========================================
def add_expense(expense):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (
                date,
                category,
                item,
                shop,
                price,
                payment
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            expense["date"],
            expense["category"],
            expense["item"],
            expense["shop"],
            expense["price"],
            expense["payment"]
        ))

        conn.commit()

        return cursor.lastrowid # 방금 INSERT한 데이터의 ID(기본 키) 반환

    finally:
        conn.close()

# ==========================================
# READ ALL
# ==========================================
def get_all_expenses():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                date,
                category,
                item,
                shop,
                price,
                payment
            FROM expenses
        """)

        rows = cursor.fetchall() # DB에서 가져온 모든 결과를 리스트로 반환

        expenses = []

        for row in rows:
            expenses.append({
                "id": row[0],
                "date": row[1],
                "category": row[2],
                "item": row[3],
                "shop": row[4],
                "price": row[5],
                "payment": row[6]
            })

        return expenses

    finally:
        conn.close()

# ==========================================
# SEARCH
# ==========================================
def get_expenses(keyword="", category="", payment=""):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        query = """
            SELECT
                id,
                date,
                category,
                item,
                shop,
                price,
                payment
            FROM expenses
            WHERE 1=1
        """

        params = []


        if keyword:
            query += """
                AND (
                    item LIKE ?
                    OR shop LIKE ?
                )
            """

            keyword_value = f"%{keyword}%"

            params.extend([
                keyword_value,
                keyword_value
            ])

        if category:
            query += """
                AND category = ?
            """

            params.append(category)

        if payment:
            query += """
                AND payment = ?
            """

            params.append(payment)

        cursor.execute(query, params)

        rows = cursor.fetchall()

        expenses = []

        for row in rows:
            expenses.append({
                "id": row[0],
                "date": row[1],
                "category": row[2],
                "item": row[3],
                "shop": row[4],
                "price": row[5],
                "payment": row[6]
            })

        return expenses

    finally:
        conn.close()

# ==========================================
# UPDATE
# ==========================================
def update_expense(expense_id, expense):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE expenses
            SET
                date = ?,
                category = ?,
                item = ?,
                shop = ?,
                price = ?,
                payment = ?
            WHERE id = ?
        """, (
            expense["date"],
            expense["category"],
            expense["item"],
            expense["shop"],
            expense["price"],
            expense["payment"],
            expense_id
        ))

        conn.commit()

    finally:
        conn.close()

# ==========================================
# DELETE
# ==========================================
def delete_expense(expense_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (
            expense_id,
        ))

        conn.commit()

    finally:
        conn.close()