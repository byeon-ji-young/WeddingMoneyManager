import tkinter as tk
from tkinter import ttk, messagebox

from database.settings import get_setting, update_setting

class BudgetDialog(tk.Toplevel):
    def __init__(self, parent, callback=None): # __init__: 팝업창 초기화 (모달 설정, 창 크기/위치 지정) / self: 이 클래스로 만든 객체 자기 자신
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.callback = callback # callback은 이 창에서 어떤 작업이 끝났을 때 부모 창에게 알려줄 함수
        
        self.title("예산 변경")
        self.geometry("350x260")
        self.resizable(False, False)

        self.configure(bg="#f8f9fa")

        self.create_widgets()
        self.load_budget()

    def create_widgets(self):
        title = ttk.Label(
            self,
            text="💰 예산 변경",
            font=("맑은 고딕", 13, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        frame = ttk.LabelFrame(
            self,
            text="예산 설정",
            padding=15
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            frame,
            text="변경할 예산"
        ).pack(anchor="w")

        self.budget_entry = ttk.Entry(
            frame,
            font=("맑은 고딕", 10)
        )

        self.budget_entry.pack(
            fill="x",
            pady=10
        )

        save_button = ttk.Button(
            self,
            text="저장",
            command=self.save_budget
        )

        save_button.pack(
            pady=15
        )

    def load_budget(self):
        budget = get_setting("budget")

        if budget:
            self.budget_entry.insert(0, f"{int(budget):,}") # insert(): entry에 글자를 넣는 함수. entry.insert(넣을 위치, 넣을 내용) / ':,': 숫자에 천 단위 콤마를 넣는 포맷

    def save_budget(self):
        value = self.budget_entry.get().replace(",", "").strip()

        if not value.isdigit():
            messagebox.showwarning("입력 오류", "숫자로 입력해주세요.", parent=self)
            return

        update_setting("budget", str(value))

        if self.callback:
            self.callback(int(value)) # self.callback(): 함수 실행
            # 자식 창이 부모 창의 함수를 직접 알 필요가 없게 만들기 위해서 사용함. 즉, callback은 나중에 실행할 함수를 미리 전달해 놓는 것

        messagebox.showinfo("저장 완료", "예산이 변경되었습니다.", parent=self)

        self.destroy() # 현재 위젯(창) 닫기