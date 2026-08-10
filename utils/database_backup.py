import shutil # 파일이나 폴더를 복사, 이동, 삭제하는 기능 제공
import sqlite3

from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox

DATABASE_FILE = Path("wedding.db")

BACKUP_DIR = Path("backup")

# 데이터 백업
def backup_database():
    if not DATABASE_FILE.exists():
        messagebox.showerror("오류", "백업할 데이터베이스가 없습니다.")
        return

    save_path = filedialog.asksaveasfilename( # filedialog.asksaveasfilename: 사용자가 어디에 저장할지 선택하는 창을 띄우기
        initialfile=f"wedding_backup_{datetime.now().strftime('%Y%m%d')}.db", # 기본 파일 이름 설정
        defaultextension=".db", # 기본 확장자
        filetypes=[("SQLite Database", "*.db")] # 파일 저장창에서 .db 파일만 보임
    )

    if not save_path: # 취소 버튼을 클릭하면 save_path가 "" 라서 함수 종료
        return

    shutil.copy(DATABASE_FILE, save_path) # shutil.copy(): 파일 복사 함수. shutil.copy(원본, 복사할 위치)

    messagebox.showinfo("완료", "데이터 백업이 완료되었습니다.")

# 데이터 검증
def is_valid_database(db_path):
    """ WeddingMoneyManager에서 사용하는 SQLite 데이터베이스인지 확인한다. """

    try:
        conn = sqlite3.connect(db_path) # db_path에 있는 SQLite 데이터베이스에 연결
        cursor = conn.cursor()
        # conn = 데이터베이스와 연결된 통로
        # cursor = 그 통로를 통해 SQL을 실행하는 도구

        # 필요한 테이블 목록
        required_tables = {
            "expenses",
            "settings",
            "categories"
        } # set 타입이라 순서는 상관 없음

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """) # SQLite의 구조 정보를 조회해서 테이블 타입의 이름만 가져와라. 조회 시 [("expenses",), ("settings",), ("categories",)] 처럼 나옴

        existing_tables = {
            row[0] # row[0]: SQL 결과가 (테이블이름,) 형태의 튜플이기 때문에 사용
            for row in cursor.fetchall()
        }

        conn.close()

        return required_tables.issubset(existing_tables) # A.issubset(B): A의 모든 항목이 B 안에 들어있는지 확인하는 것. 즉, 필요한 테이블(required_tables)이 실제 존재하는 테이블(existing_tables) 안에 전부 들어있는지 체크

    except sqlite3.Error:
        return False

# 데이터 복원
def restore_database(window, main_window):
    if not DATABASE_FILE.exists():
        messagebox.showerror("오류", "현재 데이터베이스가 없습니다.")
        return

    restore_file = filedialog.askopenfilename(
        title="복원할 데이터베이스 선택",
        filetypes=[
            ("SQLite Database", "*.db")
        ]
    )

    if not restore_file:
        return

    if not is_valid_database(restore_file):
        messagebox.showerror(
            "복원 실패",
            "선택한 파일은 WeddingMoneyManager에서\n사용할 수 있는 데이터베이스가 아닙니다."
        )

        return

    confirm = messagebox.askyesno(
        "복원 확인",
        "현재 데이터를 선택한 백업 파일로 복원합니다.\n"
        "계속하시겠습니까?"
    )

    if not confirm:
        return

    # 복원 전 현재 DB 백업
    backup_before_restore = (BACKUP_DIR / f"wedding_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

    BACKUP_DIR.mkdir(exist_ok=True) # 백업 폴더가 없으면 생성. exist_ok=True: 이미 폴더가 있어도 오류가 발생하지 않음

    # 현재 DB 백업
    shutil.copy(DATABASE_FILE, backup_before_restore) # shutil.copy(원본, 복사할 위치)

    # 선택한 백업 DB → 현재 DB
    shutil.copy(restore_file, DATABASE_FILE)

    messagebox.showinfo("완료", "데이터 복원이 완료되었습니다.\n프로그램을 다시 실행해주세요.")

    window.destroy()
    main_window.destroy()

# shutil.copy() : 파일 복사
# shutil.move() : 파일 이동
# shutil.copytree() : 폴더 전체 복사
# shutil.rmtree() : 폴더 전체 삭제