import sqlite3
import sys
from pathlib import Path

# ==========================================
# DB 위치 설정
# ==========================================
# exe 실행 시:
#   WeddingMoneyManager.exe가 있는 폴더에 wedding.db 생성
#
# py 실행 시:
#   프로젝트 루트의 wedding.db 사용

if getattr(sys, "frozen", False):  # getattr(): 객체의 속성을 가져오는 함수. getattr(객체, "속성명", 기본값) / sys.frozen 이 속성은 PyInstaller 같은 프로그램으로 exe를 만들었을 때만 생성
    # PyInstaller exe 실행 위치
    BASE_DIR = Path(sys.executable).parent # sys.executable: 현재 실행 중인 실행 파일의 경로

else:
    # 현재 프로젝트 루트
    BASE_DIR = Path(__file__).resolve().parent.parent # __file__: 현재 파이썬 파일 /  resolve(): 절대 경로 변환

DB_PATH = BASE_DIR / "wedding.db"

# ==========================================
# 연결
# ==========================================
def get_connection():
    return sqlite3.connect(DB_PATH)