import tkinter as tk
from tkinter import ttk, messagebox

from ui.category_window import CategoryWindow
from .budget_dialog import BudgetDialog

class SettingsWindow(tk.Toplevel): # 괄호 안은 상속(inheritance)을 의미. tk.Toplevel은 새로운 별도 창. 즉, Tkinter의 새 창 기능을 물려받아서 새로운 창을 만드는 클래스
    # 파이썬 규칙상, 클래스 안에서 만드는 함수(메서드)는 첫 번째 인자로 무조건 self를 받도록 약속되어 있음!
    def __init__(self, parent, callback=None): # callback=None: callback이라는 값을 하나 받겠다는 뜻
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.callback = callback

        self.title("설정")
        self.geometry("450x570")
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

        # Label
        self.style.configure(
            "TLabel",
            font=("맑은 고딕", 9),
            background="#f8f9fa",
            foreground="#495057"
        )

        # 제목 Label
        self.style.configure(
            "Title.TLabel",
            font=("맑은 고딕", 14, "bold"),
            background="#f8f9fa",
            foreground="#212529"
        )

        # LabelFrame 배경
        self.style.configure(
            "TLabelframe",
            background="#f8f9fa"
        )

        # LabelFrame 제목 스타일
        self.style.configure(
            "TLabelframe.Label",
            font=("맑은 고딕", 10, "bold"),
            foreground="#212529",
            background="#f8f9fa"
        )

        # Button
        self.style.configure(
            "TButton",
            font=("맑은 고딕", 9, "bold"),
            padding=(10, 6)
        )

    def create_widgets(self):
        # =========================
        # 제목
        # =========================
        title = ttk.Label(
            self,
            text="⚙ 설정",
            style="Title.TLabel"
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # =========================
        # 예산 관리
        # =========================
        budget_frame = ttk.LabelFrame(
            self,
            text="💰 예산 관리",
            padding=15,
        )

        budget_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        budget_label = ttk.Label(
            budget_frame,
            text="예산 설정 기능"
        )

        budget_label.pack(
            anchor="w",
            pady=(0, 10)
        )

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


        budget_button = ttk.Button(
            budget_frame,
            text="예산 변경",
            command=self.open_budget
        )

        budget_button.pack(
            fill="x"
        )

        # =========================
        # 카테고리 관리
        # =========================
        category_frame = ttk.LabelFrame(
            self,
            text="📁 카테고리 관리",
            padding=15
        )

        category_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        category_label = ttk.Label(
            category_frame,
            text="카테고리 추가 / 수정 / 삭제"
        )

        category_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        category_button = ttk.Button(
            category_frame,
            text="카테고리 관리",
            command=self.open_category
        )

        category_button.pack(
            fill="x"
        )

        # =========================
        # 데이터 관리
        # =========================
        data_frame = ttk.LabelFrame(
            self,
            text="💾 데이터 관리",
            padding=15
        )

        data_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        data_label = ttk.Label(
            data_frame,
            text="백업 / 복원 / CSV Export"
        )

        data_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        csv_button = ttk.Button(
            data_frame,
            text="CSV 내보내기",
            command=self.export_csv
        )

        csv_button.pack(
            fill="x",
            pady=3
        )

        backup_button = ttk.Button(
            data_frame,
            text="DB 백업",
            command=self.backup_db
        )

        backup_button.pack(
            fill="x",
            pady=3
        )

        restore_button = ttk.Button(
            data_frame,
            text="DB 복원",
            command=self.restore_db
        )

        restore_button.pack(
            fill="x",
            pady=3
        )

    # =====================================
    # 버튼 기능
    # =====================================
    # 예산 관리
    def open_budget(self):
        BudgetDialog(self, callback=self.callback)

    # 카테고리 관리
    def open_category(self):
        CategoryWindow(self)

    # 데이터 관리 - CSV 내보내기
    def export_csv(self):
        messagebox.showinfo(
            "CSV",
            "CSV 내보내기 기능 준비 중입니다.",
            parent=self
        )

    # 데이터 관리 - DB 백업
    def backup_db(self):
        messagebox.showinfo(
            "Backup",
            "DB 백업 기능 준비 중입니다.",
            parent=self
        )

    # 데이터 관리 - DB 복원
    def restore_db(self):
        messagebox.showinfo(
            "Restore",
            "DB 복원 기능 준비 중입니다.",
            parent=self
        )