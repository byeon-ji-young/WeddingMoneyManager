import shutil
import sys
from pathlib import Path

from .connection import get_connection, DB_PATH

# ==========================================
# PyInstaller 리소스 위치
# ==========================================
# exe 실행 시:
#   _MEIPASS 내부에 포함된 초기 DB 위치
#
# py 실행 시:
#   프로젝트 루트

if getattr(sys, "frozen", False):
    # PyInstaller 내부 포함 파일 위치 (초기 DB)
    RESOURCE_DIR = Path(sys._MEIPASS)

else:
    RESOURCE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# DB 초기 생성
# ==========================================
def create_database():
    # --------------------------------------
    # 최초 실행 시 템플릿 DB 복사
    # --------------------------------------
    # exe 실행 시:
    # - PyInstaller 내부(_internal)에 포함된 wedding.db는 초기 데이터(템플릿 DB)
    # - 실제 사용할 DB는 exe와 같은 폴더에 생성하여 유지
    #
    # 처음 실행하는 경우에만:
    # _internal/wedding.db → 프로그램 폴더/wedding.db 로 복사
    #
    # 이후 실행부터는 이미 생성된 wedding.db를 사용하기 때문에 기존 데이터가 덮어써지지 않음
    
    if not DB_PATH.exists():
        template_db = RESOURCE_DIR / "wedding.db"

        if template_db.exists():
            shutil.copy(template_db, DB_PATH)


    # --------------------------------------
    # 테이블 생성
    # --------------------------------------
    conn = get_connection() # 데이터베이스 연결

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

    except Exception as e:
        print(f"DB Error : {e}")
    
    finally:
        conn.close()