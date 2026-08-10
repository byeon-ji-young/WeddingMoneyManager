import tkinter as tk
from tkinter import ttk, messagebox

from ui.category_window import CategoryWindow
from .budget_dialog import BudgetDialog
from utils.csv_export import csv_export_file
from utils.database_backup import backup_database, restore_database

class SettingsWindow(tk.Toplevel): # 괄호 안은 상속(inheritance)을 의미. tk.Toplevel은 새로운 별도 창. 즉, Tkinter의 새 창 기능을 물려받아서 새로운 창을 만드는 클래스
    # 파이썬 규칙상, 클래스 안에서 만드는 함수(메서드)는 첫 번째 인자로 무조건 self를 받도록 약속되어 있음!
    def __init__(self, parent, callback=None): # callback=None: callback이라는 값을 하나 받겠다는 뜻
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.parent = parent
        self.callback = callback

        self.title("설정")
        self.geometry("450x500")
        self.resizable(False, False)

        self.configure(bg="#f8f9fa")

        self.setup_styles()
        self.create_widgets()

    # ttk 스타일 설정
    def setup_styles(self):
        self.style = ttk.Style(self)

        # 공통 테마
        self.style.theme_use("clam")

        # Frame
        self.style.configure("TFrame", background="#f8f9fa")

        # 제목 Label
        self.style.configure(
            "Title.TLabel",
            font=("맑은 고딕", 14, "bold"),
            background="#f8f9fa",
            foreground="#1F497D"
        )

        # 섹션 제목 Label
        self.style.configure(
            "Section.TLabel",
            font=("맑은 고딕", 10, "bold"),
            background="#f8f9fa",
            foreground="#212529"
        )

        # 서브타이틀 Label
        self.style.configure(
            "Sub.TLabel",
            font=("맑은 고딕", 9),
            background="#f8f9fa",
            foreground="#6c757d"
        )

        # 버튼
        self.style.configure(
            "TButton",
            font=("맑은 고딕", 9, "bold"),
            padding=(10, 7),
            background="#E2E8F0",
            foreground="#1e293b",
            borderwidth=0
        )
        self.style.map("TButton", background=[("active", "#CBD5E1")])

    def create_widgets(self):
        # =========================
        # 제목
        # =========================
        title = ttk.Label(
            self,
            text="⚙ 설정",
            style="Title.TLabel",
        )

        title.pack(anchor="w", padx=25, pady=(20, 15))

        # =========================
        # 예산 관리
        # =========================
        budget_frame = ttk.Frame(self, padding=(25,0))
        budget_frame.pack(fill="x")

        # 섹션 제목 + 서브타이틀
        ttk.Label(budget_frame, text="💰 예산 관리", style="Section.TLabel").pack(anchor="w")
        ttk.Label(budget_frame, text="총 예산 금액을 수정합니다.", style="Sub.TLabel").pack(anchor="w", pady=(2, 8))

        # 하단 길쭉한 버튼
        budget_button = ttk.Button(
            budget_frame,
            text="예산 변경",
            style="TButton",
            command=self.open_budget
        )
        budget_button.pack(fill="x")

        # fill: 위젯의 크기를 늘릴지 결정. 즉, 위젯의 크기
        # anchor: 위젯의 위치를 어디에 둘지 결정. 즉, 위젯의 위치
        # 
        # fill="x" → 위젯을 가로 방향으로 늘림
        # fill="y" → 위젯을 세로 방향으로 늘림
        # fill="both" → 가로·세로 모두 늘림
        # anchor="w" → 위젯을 왼쪽에 붙임
        # anchor="e" →오른쪽에 붙임
        # anchor="n" → 위쪽에 붙임
        # anchor="s" → 아래쪽에 붙임

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=25, pady=18) # 구분선

        # =========================
        # 카테고리 관리
        # =========================
        category_frame = ttk.Frame(self, padding=(25, 0))
        category_frame.pack(fill="x")

        ttk.Label(category_frame, text="📁 카테고리 관리", style="Section.TLabel").pack(anchor="w")
        ttk.Label(category_frame, text="지출 카테고리를 추가 / 수정 / 삭제합니다.", style="Sub.TLabel").pack(anchor="w", pady=(2, 8))

        category_button = ttk.Button(
            category_frame,
            text="카테고리 관리",
            style="TButton",
            command=self.open_category
        )
        category_button.pack(fill="x")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=25, pady=18)  # 구분선

        # =========================
        # 데이터 관리
        # =========================
        data_frame = ttk.Frame(self, padding=(25, 0))
        data_frame.pack(fill="x")

        ttk.Label(data_frame, text="💾 데이터 관리", style="Section.TLabel").pack(anchor="w")
        ttk.Label(data_frame, text="데이터를 파일로 내보내거나 DB를 백업/복원합니다.", style="Sub.TLabel").pack(anchor="w", pady=(2, 8))

        # 하단 버튼 그룹
        csv_button = ttk.Button(
            data_frame,
            text="📊 CSV 저장",
            style="TButton",
            command=self.export_csv
        )
        csv_button.pack(fill="x", pady=(0, 5))

        backup_button = ttk.Button(
            data_frame,
            text="📦 DB 백업",
            style="TButton",
            command=self.backup_db
        )
        backup_button.pack(fill="x", pady=5)

        restore_button = ttk.Button(
            data_frame,
            text="🔄 DB 복원",
            style="TButton",
            command=self.restore_db
        )
        restore_button.pack(fill="x", pady=(5, 0))

    # =====================================
    # 버튼 기능
    # =====================================
    # 예산 관리
    def open_budget(self):
        BudgetDialog(self, callback=self.callback)

    # 카테고리 관리
    def open_category(self):
        CategoryWindow(self)

    # 데이터 관리 - CSV 저장
    def export_csv(self):
        csv_export_file()

    # 데이터 관리 - DB 백업
    def backup_db(self):
        backup_database()

    # 데이터 관리 - DB 복원
    def restore_db(self):
        # messagebox.showinfo("Restore", "DB 복원 기능 준비 중입니다.", parent=self)
        restore_database(self, self.parent)