import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class ExpenseDialog(tk.Toplevel):
    def __init__(self, parent, title="지출 입력", initial_data=None): # __init__: 팝업창 초기화 (모달 설정, 창 크기/위치 지정) / self: 이 클래스로 만든 객체 자기 자신
        # 파이썬 규칙상, 클래스 안에서 만드는 함수(메서드)는 첫 번째 인자로 무조건 self를 받도록 약속되어 있음!
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정
        self.title(title)
        self.geometry("300x460")
        self.configure(bg="#F4F6F9")
        self.resizable(False, False)

        # 부모 창 위에 항상 유지 & 모달(Modal) 설정
        # 모달 창으로 만드는 핵심 설정. 이 팝업이 떠 있으면 메인 창 클릭 못하게 만드는 역할
        self.transient(parent)
        self.grab_set()

        self.result = None # self.result: 입력하거나 수정 완료한 데이터(딕셔너리)를 담아서 메인 창으로 돌려줄 변수. 초기값은 None
        self.initial_data = initial_data

        self.create_widgets()

        if self.initial_data:
            self.load_initial_data()

        # 창 중앙 정렬
        self.center_window(parent)

    # 팝업 창 위치 조절
    def center_window(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)

        self.geometry(f"+{x}+{y}")

    # 팝업 내부 입력 칸, 버튼 UI 생성
    def create_widgets(self):
        container = tk.Frame(self, bg="white", padx=20, pady=20)
        container.pack(fill="both", expand=True, padx=15, pady=15) 
        # fill="x" : 가로 방향으로 부모 크기에 맞게 늘어남 / "y" : 세로 방향으로 늘어남 / "both" : 가로와 세로 모두 늘어남
        # expand는 부모 창에 남는 공간을 위젯이 가져갈지 결정. true면 남는 공간이 있을 경우 이 위젯에게 배분함

        # 입력 항목 스타일 공통 지정
        label_style = {"font": ("맑은 고딕", 9, "bold"), "bg": "white", "fg": "#475569"}
        entry_style = {"font": ("맑은 고딕", 10), "relief": "solid", "bd": 1} # relief: 위젯의 테두리 모양 옵션. "solid": 실선, "flat": 테두리 없음 ...

        # 1. 날짜 입력
        tk.Label(container, text="날짜", **label_style).grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.date_entry = DateEntry(container, date_pattern="yyyy-mm-dd", width=28, **entry_style)
        self.date_entry.grid(row=1, column=0, pady=(0, 12), sticky="ew")
        # sticky="w" : 왼쪽(west)에 붙임 / "e": 오른쪽(east)에 붙임 / "n": 위쪽(north)에 붙임 / "s": 아래쪽(sount)에 붙임 ex) "ex": 왼쪽과 오른쪽에 모두 붙어라

        # self.date_entry 라고 적었기 때문에 이 클래스 안의 다른 메서드에서도 접근 가능해짐

        # 2. 분류 선택
        tk.Label(container, text="분류", **label_style).grid(row=2, column=0, sticky="w", pady=(0, 2))
        self.category_combo = ttk.Combobox(
            container,
            values=["예식장", "스드메", "스냅영상", "맞춤정장", "예물", "신혼여행", "가전", "가구", "생활용품", "기타"],
            # state="readonly",
            width=28,
        )
        self.category_combo.grid(row=3, column=0, pady=(0, 12), sticky="ew")
        # self.category_combo.current(0)

        # 3. 항목 입력
        tk.Label(container, text="항목", **label_style).grid(row=4, column=0, sticky="w", pady=(0, 2))
        self.item_entry = tk.Entry(container, **entry_style)
        self.item_entry.grid(row=5, column=0, pady=(0, 12), sticky="ew")

        # 4. 구매처 입력 및 선택
        tk.Label(container, text="구매처", **label_style).grid(row=6, column=0, sticky="w", pady=(0, 2))
        self.shop_combo = ttk.Combobox(
            container,
            values=["오늘의집", "쿠팡", "이케아", "한샘", "리바트", "삼성스토어", "LG베스트샵", "기타"],
            width=28,
        )
        self.shop_combo.grid(row=7, column=0, pady=(0, 12), sticky="ew")

        # 5. 금액 입력
        tk.Label(container, text="금액", **label_style).grid(row=8, column=0, sticky="w", pady=(0, 2))
        self.price_entry = tk.Entry(container, **entry_style)
        self.price_entry.grid(row=9, column=0, pady=(0, 12), sticky="ew")
        self.price_entry.bind("<KeyRelease>", self.format_price)

        # "<KeyRelease>" → 일반 이벤트 (기본 이벤트)

        # 6. 결제수단 선택
        tk.Label(container, text="결제수단", **label_style).grid(row=10, column=0, sticky="w", pady=(0, 2))
        self.payment_combo = ttk.Combobox(
            container,
            values=["신용카드", "체크카드", "현금", "계좌이체"],
            state="readonly",
            width=28,
        )
        self.payment_combo.grid(row=11, column=0, pady=(0, 15), sticky="ew")
        self.payment_combo.current(0)

        # 버튼 영역
        btn_frame = tk.Frame(container, bg="white")
        btn_frame.grid(row=12, column=0, sticky="ew", pady=(10, 0))

        save_btn = tk.Button(
            btn_frame, 
            text="저장", 
            command=self.on_save,
            font=("맑은 고딕", 9, "bold"), 
            bg="#2563EB", 
            fg="white",
            relief="flat", 
            bd=0, 
            cursor="hand2", 
            width=12, 
            pady=6
        )
        save_btn.pack(side="left", expand=True, padx=(0, 5))

        cancel_btn = tk.Button(
            btn_frame, 
            text="취소", 
            command=self.destroy,
            font=("맑은 고딕", 9, "bold"), 
            bg="#64748B", 
            fg="white",
            relief="flat", 
            bd=0, 
            cursor="hand2", 
            width=12, 
            pady=6
        )
        cancel_btn.pack(side="right", expand=True, padx=(5, 0))

    # 금액 자동 콤마 포맷팅 함수 (커서 위치 유지)
    def format_price(self, event=None):
        # 숫자만 추출
        numbers = "".join(filter(str.isdigit, self.price_entry.get())) # filter(str.isdigit, text): 숫자만 남기기 위해 사용

        # 비어있으면 종료
        if not numbers:
            self.price_entry.delete(0, tk.END)
            return

        # 현재 숫자의 개수
        digit_pos = len("".join(filter(str.isdigit, self.price_entry.get()[: self.price_entry.index(tk.INSERT)]))) # price_entry.get()[:tk.INSERT]: 현재 커서 앞까지만 자른다 / "".join(...): 다시 문자열로 만든다

        # 콤마 추가
        formatted = f"{int(numbers):,}"

        # 다시 출력
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, formatted)

        # 숫자 개수를 기준으로 커서 위치 계산
        count = 0
        cursor = len(formatted)

        for idx, char in enumerate(formatted):
            if char.isdigit():
                count += 1
            if count == digit_pos:
                cursor = idx + 1
                break
        self.price_entry.icursor(cursor)

    # 기존 데이터를 입력 칸에 채우기
    def load_initial_data(self):
        self.date_entry.set_date(self.initial_data["date"])
        self.category_combo.set(self.initial_data["category"])
        self.item_entry.insert(0, self.initial_data["item"])
        self.shop_combo.set(self.initial_data.get("shop", ""))
        self.price_entry.insert(0, f"{self.initial_data['price']:,}")
        self.payment_combo.set(self.initial_data.get("payment", ""))

    # 데이터 검증 후 메인 창으로 데이터 전달
    def on_save(self):
        # create_widgets에서 만든 date_entry 값을 여기서 가져올 수 있음
        date = self.date_entry.get()
        category = self.category_combo.get()
        item = self.item_entry.get().strip()
        shop = self.shop_combo.get().strip()
        price_str = self.price_entry.get().replace(",", "").strip()
        payment = self.payment_combo.get()
            
        if not item or not price_str:
            messagebox.showwarning("입력 오류", "항목과 금액을 입력하세요.", parent=self) # parent=self: 사용자가 경고를 확인하기 전까지 부모 창을 계속 조작하지 못하게 하는 일반적인 동작을 제공
            return

        try:
            price = int(price_str)
        except ValueError:
            messagebox.showwarning("입력 오류", "금액은 숫자로 입력하세요.", parent=self)
            return

        self.result = {
            "date": date if date else datetime.today().strftime("%Y-%m-%d"),
            "category": category if category else "기타",
            "item": item,
            "shop": shop,
            "price": price,
            "payment": payment if payment else "미선택",
        } # Python의 dictionary(딕셔너리)

        self.destroy()