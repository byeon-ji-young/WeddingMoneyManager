import tkinter as tk
from tkinter import ttk, messagebox

from database.settings import get_setting, update_setting

class BudgetDialog(tk.Toplevel):
    def __init__(self, parent, callback=None): # __init__: 팝업창 초기화 (모달 설정, 창 크기/위치 지정) / self: 이 클래스로 만든 객체 자기 자신
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.callback = callback # callback은 이 창에서 어떤 작업이 끝났을 때 부모 창에게 알려줄 함수
        
        self.title("예산 변경")
        self.geometry("350x200")
        self.resizable(False, False)

        self.configure(bg="#f8f9fa")

        self.create_widgets()
        self.load_budget()

    def create_widgets(self):
        # =========================
        # 타이틀
        # =========================
        title = ttk.Label(
            self,
            text="💰 예산 변경",
            font=("맑은 고딕", 12, "bold"),
            background="#f8f9fa",
            foreground="#1F497D"
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # =========================
        # 입력 영역
        # =========================
        form_frame = tk.Frame(self, bg="#f8f9fa")
        form_frame.pack(fill="x", padx=25)

        tk.Label(
            form_frame,
            text="변경할 예산",
            font=("맑은 고딕", 9, "bold"),
            bg="#f8f9fa",
            fg="#495057"
        ).pack(anchor="w", pady=(0, 6))

        # 입력창 + '원' 단위 가로 배치 프레임
        entry_frame = tk.Frame(form_frame, bg="#f8f9fa")
        entry_frame.pack(fill="x")

        self.budget_entry = ttk.Entry(
            entry_frame,
            font=("맑은 고딕", 10),
            justify="right" # 금액 입력이므로 우측 정렬
        )
        self.budget_entry.pack(side="left", fill="x", expand=True, ipady=2)

        unit_label = tk.Label(
            entry_frame,
            text=" 원",
            font=("맑은 고딕", 10, "bold"),
            bg="#f8f9fa",
            fg="#212529"
        )
        unit_label.pack(side="right")

        # =========================
        # 저장 버튼
        # =========================
        save_button = tk.Button(
            self,
            text="저장",
            font=("맑은 고딕", 9, "bold"),
            bg="#1F497D",
            fg="#ffffff",
            activebackground="#1B3E68",
            activeforeground="#ffffff",
            bd=0,
            command=self.save_budget
        )

        save_button.pack(
            fill="x",
            padx=25,
            pady=(25, 0),
            ipady=6 # ipady: internal padding Y. 즉, 위아래 내부 여백
        )

    def load_budget(self):
        budget = get_setting("budget")

        if budget:
            self.budget_entry.insert(0, f"{int(budget):,}") # insert(): entry에 글자를 넣는 함수. entry.insert(넣을 위치, 넣을 내용) / ':,': 숫자에 천 단위 콤마를 넣는 포맷

    def save_budget(self):
        value = self.budget_entry.get().replace(",", "").strip()

        if not value:
            messagebox.showwarning("입력 오류", "예산을 입력해주세요.", parent=self)
            return

        if not value.isdigit():
            messagebox.showwarning("입력 오류", "숫자로 입력해주세요.", parent=self)
            return

        update_setting("budget", str(value))

        if self.callback:
            self.callback(int(value)) # self.callback(): 함수 실행
            # 자식 창이 부모 창의 함수를 직접 알 필요가 없게 만들기 위해서 사용함. 즉, callback은 나중에 실행할 함수를 미리 전달해 놓는 것

        messagebox.showinfo("저장 완료", "예산이 변경되었습니다.", parent=self)

        self.destroy() # 현재 위젯(창) 닫기