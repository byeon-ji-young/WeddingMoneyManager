import sqlite3
import sys
import shutil
from pathlib import Path

# ==========================================
# DB 설정
# ==========================================
# 실행 파일(.exe)이면 exe가 있는 폴더를 기준으로 사용하고, 파이썬 파일(.py)이면 현재 파일이 있는 폴더를 기준으로 사용
if getattr(sys, 'frozen', False): # getattr(): 객체의 속성을 가져오는 함수. getattr(객체, "속성명", 기본값) / sys.frozen 이 속성은 PyInstaller 같은 프로그램으로 exe를 만들었을 때만 생성
    # exe 실행 위치 (사용자 DB 저장 위치)
    BASE_DIR = Path(sys._MEIPASS).parent # sys.executable: 현재 실행 중인 실행 파일의 경로

    # PyInstaller 내부 포함 파일 위치 (초기 DB)
    RESOURCE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent # __file__: 현재 파이썬 파일 /  resolve(): 절대 경로 변환

    RESOURCE_DIR = BASE_DIR
    
DB_PATH = BASE_DIR / "wedding.db"

# ==========================================
# 연결
# ==========================================
def get_connection():
    return sqlite3.connect(DB_PATH)

# ==========================================
# 초기 생성
# ==========================================
def create_database():
    # exe 실행 시:
    # - PyInstaller 내부(_internal)에 포함된 wedding.db는 초기 데이터(템플릿 DB)
    # - 실제 사용할 DB는 exe와 같은 폴더에 생성하여 유지
    #
    # 처음 실행하는 경우에만:
    # _internal/wedding.db → 프로그램 폴더/wedding.db 로 복사
    #
    # 이후 실행부터는 이미 생성된 wedding.db를 사용하기 때문에
    # 기존 데이터가 덮어써지지 않음
    if not DB_PATH.exists():
        template_db = RESOURCE_DIR / "wedding.db"

        if template_db.exists():
            shutil.copy(template_db, DB_PATH)

    # 데이터베이스 연결
    conn = get_connection()  

    try:
        cursor = conn.cursor() # Python -> cursor -> SQLite. (cursor는 데이터베이스와 대화하는 객체)

        # cursor.execute(): SQL 명령을 실행하는 함수
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                item TEXT NOT NULL,
                shop TEXT,
                price INTEGER NOT NULL,
                payment TEXT
            )
        """)
        # """...""", '''...''' : 여러 줄 문자열에 사용 (SQL, 긴 문장, 설명 등에 적합)
        # "...", '...' : 일반적인 문자열에 주로 사용
    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO settings(key, value)
            VALUES ('budget', '60000000')
        """)
        
        conn.commit()

    # except Exception as e:
    except sqlite3.Error as e:
        print(f"DB Error : {e}")
            
    finally:
        conn.close()

# ==========================================
# expenses table
# ==========================================
# CREATE
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

        return cursor.lastrowid
    finally:
        conn.close()

# READ
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

# SEARCH
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
            params.extend([keyword_value, keyword_value])

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

# UPDATE
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

# DELETE
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

# ==========================================
# settings table
# ==========================================
# READ
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

# UPDATE
def update_setting(key, value):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO settings(key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
        """, (key, str(value)))

        conn.commit()

    finally:
        conn.close()


# ==========================================
# 직접 실행할 때만 실행
# ==========================================
if __name__ == "__main__": # 직접 실행할 때만 실행되고, import할 때는 실행되지 않음
    create_database()

    expenses = get_all_expenses()

    for expense in expenses:
        print(expense)

    print("-- success --")

# __name__: Python 파일마다 자동으로 만들어지는 특별한 변수 ★
# database.py, excel_export.py, statistics.py 같은 모듈 파일에는 if __name__ == "__main__": 패턴을 쓰는 게 좋은 습관