import shutil # 파일이나 폴더를 복사, 이동, 삭제하는 기능 제공
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