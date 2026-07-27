import tkinter as tk # GUI를 만들기 위한 tkinter 라이브러리 불러오기
from tkinter import messagebox # tkinter 안에 있는 messagebox 기능 가져와줘

import json

from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk

import matplotlib.pyplot as plt # 그래프를 만들기 위한 matplotlib 라이브러리 불러오기 (pyplot: 그래프 그리는 기능)
import matplotlib.font_manager as fm

# Matplotlib 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic" # or plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# ==========================================
# 전역 변수
# ==========================================
money_data = []
selected_index = None
budget = 30000000
price_reverse = False
sort_reverse = {
    "date": False,
    "category": False,
    "item": False,
    "price": False
}
progress_value = 0


# ==========================================
# 메인 윈도우(창) 생성
# ==========================================
window = tk.Tk()
window.title("💒 신혼 자금 관리") # 창 제목
window.geometry("820x920") # 창 크기 (widthxheight)
# window.state("zoomed") # 창 크기 최대화
window.configure(bg="#F4F6F9")

# Tkinter 스타일 설정
style = ttk.Style()
style.theme_use("clam")


# ==========================================
# 1. 헤더 타이틀 영역 (Top Header)
# ==========================================
# 1. pack() : 자동 배치
# 2. grid() : 행(row), 열(column) 기준 배치
# 3. place() : 좌표(x, y) 기준 배치

header_frame = tk.Frame(window, bg="#F4F6F9")
header_frame.pack(fill="x", padx=30, pady=(20, 10)) # fill="x" : 가로 방향으로 부모 크기에 맞게 늘어남 / "y" : 세로 방향으로 늘어남 / "both" : 가로와 세로 모두 늘어남
# padx: 위젯 바깥쪽의 가로(좌우) 여백 / ipadx: 위젯 안쪽의 좌우 여백(위젯 자체의 너비를 늘림) / pady: 위젯 바깥쪽의 세로(상하) 여백

title_label = tk.Label(
    header_frame,
    text="💍 예식 비용 관리 Dashboard",
    font=("맑은 고딕", 16, "bold"),
    bg="#F4F6F9",
    fg="#1E293B"
)
# title_label.pack(side="left") # "left" : 왼쪽부터 배치 / "right" : 오른쪽부터 배치 / "top" : 위쪽부터 배치(기본값) / "bottom" : 아래쪽부터 배치
title_label.pack(anchor="w", pady=(0, 15))

# 예산 설정 영역
budget_frame = tk.Frame(header_frame, bg="#F4F6F9")
# budget_frame.pack(side="right")
budget_frame.pack(anchor="w")

budget_label = tk.Label(budget_frame, text="총 예산 :", font=("맑은 고딕", 9, "bold"), bg="#F4F6F9", fg="#64748B")
budget_label.pack(side="left", padx=(0, 8))

budget_entry = tk.Entry(budget_frame, font=("맑은 고딕", 10), width=12, relief="solid", bd=1)
budget_entry.pack(side="left", padx=(0, 8))

budget_button = tk.Button(
    budget_frame, 
    text="적용", 
    command=lambda: update_budget(),
    font=("맑은 고딕", 8, "bold"), 
    bg="#334155", 
    fg="white", 
    activeforeground="white",
    activebackground="#1E293B", 
    relief="flat", 
    bd=0, 
    padx=8, 
    pady=2
)
budget_button.config(cursor="hand2") # 버튼 설정 추가하고 싶으면 config()로 추가해도 됨
budget_button.pack(side="left")


# ==========================================
# 2. 요약 카드 영역 (Dashboard Summary Cards)
# ==========================================
dashboard_frame = tk.Frame(window, bg="#F4F6F9")
dashboard_frame.pack(fill="x", padx=30, pady=10)

def create_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg="white",
        height=85,
        highlightbackground="#E2E8F0", # 포커스가 없을 때 테두리 (highlightcolor: 포커스가 있을 때 테두리 색)
        highlightthickness=1 # 강조 테두리 두께
    )
    card.pack_propagate(False) # 내부 위젯 크기에 따라 상자가 줄어들지 않게 고정

    title_lbl = tk.Label(card, text=title, font=("맑은 고딕", 9, "bold"), bg="white", fg="#64748B")
    title_lbl.pack(anchor="w", padx=15, pady=(12, 2)) # anchor="w" : 왼쪽(west)에 붙임 / "e": 오른쪽(east)에 붙임 / "n": 위쪽(north)에 붙임 / "s": 아래쪽(sount)에 붙임 / "center": 가운데에 붙임

    val_lbl = tk.Label(card, text=value, font=("맑은 고딕", 13, "bold"), bg="white", fg=color)
    val_lbl.pack(anchor="w", padx=15)

    return card, val_lbl

# 3개의 대시보드 카드 생성 (1:1:1 비율)
# columnconfigure: Frame이나 Window의 Column의 속성을 설정하는 함수 => 부모위젯.columnconfigure(열번호, 옵션)
dashboard_frame.columnconfigure(0, weight=1) # weight가 커지면 더 많은 공간 비율을 차지. 만약 0이면 창이 커져도 열의 크기는 유지
dashboard_frame.columnconfigure(1, weight=1)
dashboard_frame.columnconfigure(2, weight=1)

budget_card, budget_value = create_card(dashboard_frame, "💰 총 예산", f"{budget:,}원", "#2563EB")
used_card, used_value = create_card(dashboard_frame, "💸 현재 지출", "0원", "#DC2626")
remain_card, remain_value = create_card(dashboard_frame, "💵 남은 금액", f"{budget:,}원", "#16A34A")

budget_card.grid(row=0, column=0, padx=(0, 5), sticky="ew") # sticky="w" : 왼쪽(west)에 붙임 / "e": 오른쪽(east)에 붙임 / "n": 위쪽(north)에 붙임 / "s": 아래쪽(sount)에 붙임 ex) "ex": 왼쪽과 오른쪽에 모두 붙어라
used_card.grid(row=0, column=1, padx=5, sticky="ew")
remain_card.grid(row=0, column=2, padx=(5, 0), sticky="ew")

# anchor : 위젯 내부(or 배정된 공간)에서 내용(텍스트 등)을 어디에 붙일지 결정
# sticky : grid 셀 안의 위젯에서 위젯을 어디에 붙이고 얼마나 늘릴지 결정
# => anchor은 내용의 정렬, sticky는 위젯의 배치와 확장 개념

# 예산 진행률
progress = ttk.Progressbar(
    dashboard_frame,
    orient="horizontal", # horizontal: 가로
    mode="determinate", # determinate: 진행률이 있는 바(몇 %인지 표시). indeterminate: 왔다 갔다 하는 로딩바
    style="Green.Horizontal.TProgressbar"
)
progress.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
style.configure(
    "Green.Horizontal.TProgressbar",
    troughcolor="#E5E7EB", # 안채워진 부분 색
    background="#22C55E" # 채워진 부분 색
)

style.configure(
    "Orange.Horizontal.TProgressbar",
    troughcolor="#E5E7EB",
    background="#F59E0B"
)

style.configure(
    "Red.Horizontal.TProgressbar",
    troughcolor="#E5E7EB",
    background="#EF4444"
)

progress_status = tk.Label(dashboard_frame, text="예산 사용률 0%", font=("맑은 고딕", 10), bg="#F4F6F9", fg="#64748B")
progress_status.grid(row=2, column=0, columnspan=3, pady=(5, 10))

# ==========================================
# 3. 데이터 입력 영역 (Input Form)
# ==========================================
input_frame = tk.Frame(
    window,
    bg="white",
    padx=20,
    pady=15,
    # highlightbackground="#E2E8F0", # 포커스가 없을 때 테두리 (highlightcolor: 포커스가 있을 때 테두리 색)
    # highlightthickness=1 # 강조 테두리 두께
    highlightthickness=0
)
input_frame.pack(fill="x", padx=30, pady=10)

input_title = tk.Label(input_frame, text="💸 지출 내역 입력", font=("맑은 고딕", 11, "bold"), bg="white", fg="#1E293B")
input_title.pack(anchor="w", pady=(0, 10))

fields_frame = tk.Frame(input_frame, bg="white")
fields_frame.pack(fill="x")

# 입력 항목 스타일 공통 지정
label_style = {"font": ("맑은 고딕", 9, "bold"), "bg": "white", "fg": "#475569"}
entry_style = {"font": ("맑은 고딕", 10), "relief": "solid", "bd": 1} # relief: 위젯의 테두리 모양 옵션. "solid": 실선, "flat": 테두리 없음 ...

# 1. 날짜
date_label = tk.Label(fields_frame, text="날짜", **label_style).grid(row=0, column=0, padx=(0, 5), sticky="w")
date_entry = DateEntry(fields_frame, date_pattern="yyyy-mm-dd", width=12, **entry_style)
date_entry.grid(row=0, column=1, padx=(0, 15), pady=5)

# 2. 분류
tk.Label(fields_frame, text="분류", **label_style).grid(row=0, column=2, padx=(0, 5), sticky="w")
style.configure("Custom.TCombobox", font=("맑은 고딕", 10), padding=3)
category_combo = ttk.Combobox(
    fields_frame, 
    values=["가구", "가전", "생활용품", "여행", "예식장", "스드메", "기타"], 
    # state="readonly", 
    style="Custom.TCombobox", 
    width=12
)
category_combo.grid(row=0, column=3, padx=(0, 15), pady=5)

# 3. 항목
tk.Label(fields_frame, text="항목", **label_style).grid(row=0, column=4, padx=(0, 5), sticky="w")
item_entry = tk.Entry(fields_frame, width=15, **entry_style)
item_entry.grid(row=0, column=5, padx=(0, 15), pady=5)

# 4. 구매처
tk.Label(fields_frame, text="구매처", **label_style).grid(row=0, column=6, padx=(0, 5), sticky="w")
shop_entry = ttk.Combobox(
    fields_frame,
    values=["오늘의집", "쿠팡", "이케아", "한샘", "리바트", "삼성스토어", "LG베스트샵", "기타"],
    width=15
)
shop_entry.grid(row=0, column=7, padx=(0, 5), pady=5)

# 5. 금액
tk.Label(fields_frame, text="금액", **label_style).grid(row=1, column=0, padx=(0, 5), sticky="w")
price_entry = tk.Entry(fields_frame, width=20, **entry_style)
price_entry.grid(row=1, column=1, padx=(0, 5), pady=5)

# 버튼 영역 (입력창 하단)
btn_group = tk.Frame(input_frame, bg="white")
btn_group.pack(anchor="e", pady=(10, 0))

normal_button = {
    "font": ("맑은 고딕", 9, "bold"),
    "width": 8,
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white"
}

add_button = tk.Button(btn_group, text="➕ 추가", command=lambda: add_money(), bg="#16A34A", activebackground="#15803D", **normal_button) 
# lambda 사용하는 이유: 클릭했을 때 실행하라는 의미. command=add_money() 이렇게 쓰면 프로그램 시작할 때 바로 실행
# lambda 사용 안하려면 command=add_money 까지만 작성
add_button.pack(side="left", padx=3) # side="left": 왼쪽부터 배치하라. 기본값은 top

update_button = tk.Button(btn_group, text="✏ 수정", command=lambda: update_money(), bg="#2563EB", activebackground="#1D4ED8", **normal_button)
update_button.pack(side="left", padx=3)

delete_button = tk.Button(btn_group, text="🗑 삭제", command=lambda: delete_money(), bg="#DC2626", activebackground="#B91C1C", **normal_button)
delete_button.pack(side="left", padx=3)


# ==========================================
# 4. 목록 및 검색 영역 (Treeview & Search)
# ==========================================
list_frame = tk.Frame(window, bg="#F4F6F9")
list_frame.pack(fill="both", expand=True, padx=30, pady=10) # expand는 부모 창에 남는 공간을 위젯이 가져갈지 결정. true면 남는 공간이 있을 경우 이 위젯에게 배분함

# 검색 바 (Search Bar)
search_frame = tk.Frame(list_frame, bg="#F4F6F9")
search_frame.pack(fill="x", pady=(0, 8))

search_entry = tk.Entry(search_frame, font=("맑은 고딕", 10), relief="solid", bd=1)
search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

search_button = tk.Button(
    search_frame, 
    text="🔍 검색", 
    command=lambda: search_money(),
    font=("맑은 고딕", 9, "bold"), 
    bg="#475569", 
    fg="white", 
    activeforeground="white", # active 상태일 때 글자색 (active 상태란 마우스 오버 or 마우스 클릭)
    activebackground="#334155", # active 상태일 때 배경색
    relief="flat", 
    bd=0, 
    cursor="hand2", 
    width=8
)
search_button.pack(side="right")

# 표(Treeview) 디자인 세부 설정
# 데이터 영역(행/셀)
style.configure("Treeview", font=("맑은 고딕", 10), rowheight=30, background="white", fieldbackground="white", borderwidth=0) # background: 전체 배경 색 / fieldbackground: 각 셀의 배경색
# 헤더 영역
style.configure("Treeview.Heading", font=("맑은 고딕", 10, "bold"), background="#E2E8F0", foreground="#333333", relief="flat")
# 상태(선택됨, 눌림 등)에 따른 변화
style.map("Treeview", background=[("selected", "#E0F2FE")], foreground=[("selected", "#0369A1")])

tree_container = tk.Frame(list_frame, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
tree_container.pack(fill="both", expand=True)

money_list = ttk.Treeview(tree_container, columns=("date", "category", "item", "shop", "price"), show="headings", height=8) # show="headings": 트리 표시(#0 컬럼)는 숨기고, 컬럼 제목(heading)만 보여줘라. 기본값은 tree
scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=money_list.yview) # money_list.yview: Treeview → Scrollbar. 스크롤바 움직이면 Treeview의 세로 위치를 바꿔라
money_list.configure(yscrollcommand=scrollbar.set) # scrollbar.set: Scrollbar → Treeview. Treeview가 현재 위치를 스크롤바에 알려줘라

money_list.heading("date", text="날짜", command=lambda: sort_column("date"))
money_list.heading("category", text="분류", command=lambda: sort_column("category"))
money_list.heading("item", text="항목", command=lambda: sort_column("item"))
money_list.heading("shop", text="구매처", command=lambda: sort_column("shop"))
money_list.heading("price", text="금액", command=lambda: sort_column("price"))

money_list.column("date", width=110, anchor="center")
money_list.column("category", width=90, anchor="center")
money_list.column("item", width=250, anchor="w", stretch=True) # stretch=True: 가용 공간을 채움
money_list.column("shop", width=130, anchor="center", stretch=True)
money_list.column("price", width=120, anchor="e")

money_list.bind("<<TreeviewSelect>>", lambda event: select_money(event)) # lambda event: select_money(event) 대신 select_money만 적어도 됨

money_list.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ==========================================
# 5. 하단 통계 및 합계 영역 (Footer)
# ==========================================
footer_frame = tk.Frame(window, bg="#F4F6F9")
footer_frame.pack(fill="x", padx=30, pady=(5, 20))

total_label = tk.Label(footer_frame, text="총 지출 : 0원", font=("맑은 고딕", 11, "bold"), bg="#F4F6F9", fg="#1E293B")
total_label.pack(side="left")
# side: 위젯을 어느 방향으로 배치할지 (side는 pack()에서만 사용하는 옵션)
# anchor: 배치된 공간 안에서 위젯(또는 내용)을 어느 쪽에 붙일지

stat_btn_frame = tk.Frame(footer_frame, bg="#F4F6F9")
stat_btn_frame.pack(side="right")

bar_button = tk.Button(
    stat_btn_frame, text="📈 지출 비교", command=lambda: show_bar_chart(),
    font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
    activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
)
bar_button.pack(side="left", padx=3)

pie_button = tk.Button(
    stat_btn_frame, text="📊 카테고리 비율", command=lambda: show_pie_chart(),
    font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
    activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
)
pie_button.pack(side="left", padx=3)

# category_stats_button = tk.Button(
#     stat_btn_frame, text="통계", command=lambda: show_category_state(),
#     font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
#     activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
# )
# category_stats_button.pack(side="left", padx=3)
# month_stats_button = tk.Button(
#     stat_btn_frame, text="월별 통계", command=lambda: show_month_state(),
#     font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
#     activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
# )
# month_stats_button.pack(side="left", padx=3)
# detail_stats_button = tk.Button(
#     stat_btn_frame, text="상세 통계", command=lambda: show_detail_state(),
#     font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
#     activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
# )
# detail_stats_button.pack(side="left", padx=3)

# ==========================================
# 함수 영역 
# ==========================================
def add_money():
    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    shop = shop_entry.get()
    price = price_entry.get()

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    if item == "" or price == "":
        messagebox.showwarning("입력 오류", "항목과 금액을 입력하세요.")
        return

    try:
        price = int(price.replace(",", ""))
    except:
        messagebox.showwarning("입력 오류", "금액은 숫자로 입력하세요.")
        return

    # 실제 데이터 추가
    money_data.append({
        "date": date,
        "category": category if category else "기타",
        "item": item,
        "shop": shop,
        "price": price
    }) # Python의 dictionary(딕셔너리)
    
    save_data()
    display_data()
    update_total()

    refresh_input_entry() # 입력창 초기화

def animate_progress(target):
    global progress_value

    target = min(target, 100) # 더 작은 값 반환

    # 목표까지 남은 거리
    diff = target - progress_value

    # 거의 도착했으면 종료
    if abs(diff) < 0.3: # 절댓값(absolute value) 반환
        progress_value = target
        progress["value"] = progress_value
        return

    # 남은 거리의 20%만 이동 (처음엔 빠르고 끝에는 느림)
    progress_value += diff * 0.2

    progress["value"] = progress_value

    window.after(15, lambda: animate_progress(target)) # 15ms(0.015초) 뒤에 다시 함수 실행

def update_total():
    total = 0

    for money in money_data:
        # total += int(money["price"]) try/except 문으로 숫자 검증했으니까 바로 저장 가능
        total += money["price"]

    total_label.config(text=f"총 지출 : {total:,}원") # config: 이미 만들어진 위젯의 설정 변경

    if budget > 0:
        rate = total / budget * 100
    else:
        rate = 0

    remain = budget - total

    budget_value.config(text=f"{budget:,}원")
    used_value.config(text=f"{total:,}원\n({rate:.1f}%)")
    remain_value.config(text=f"{remain:,}원")

    # Progressbar
    progress["value"] = min(rate, 100)

    # 상태 표시
    if rate < 70:
        progress.configure(style="Green.Horizontal.TProgressbar")

        progress_status.config(
            text=f"✅ 예산의 {rate:.1f}%를 사용했습니다.",
            fg="#16A34A"
        )

    elif rate < 100:
        progress.configure(style="Orange.Horizontal.TProgressbar")

        progress_status.config(
            text=f"⚠ 예산의 {rate:.1f}%를 사용했습니다.",
            fg="#F59E0B"
        )

    else:
        progress.configure(style="Red.Horizontal.TProgressbar")

        over = total - budget

        progress_status.config(
            text=f"🚨 예산을 {over:,}원 초과했습니다.",
            fg="#DC2626"
        )

    animate_progress(rate)

def delete_money():
    selected = money_list.selection()

    if not selected:
        messagebox.showwarning("삭제 오류", "삭제할 항목을 선택하세요.")
        return
    
    if selected:
        result = messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?")

        if not result:
            return

        selected_id = selected[0]
        index = int(selected_id)

        money_data.pop(index) # 실제 데이터 삭제
        money_list.delete(selected_id) # Treeview 화면에서 삭제

        save_data()
        display_data() # 삭제 후 인덱스 재배치
        update_total()

        refresh_input_entry() # 입력창 초기화

def save_data():
    # with: 열고 → 사용하고 → 자동 정리
    with open("money.json", "w", encoding="utf-8") as file: # open(): money.json 파일을 쓰기 모드로 열어줘 (w:새로 쓰기, r:읽기, a:이어 쓰기), as file: 열린 파일을 file이라는 이름으로 사용
        json.dump( # json.dump(): Python 데이터를 JSON 파일로 저장
            {
                "budget": budget,
                "money_data": money_data
            },
            file,
            ensure_ascii=False, # 한글을 그대로 저장(true로 하면 유니코드로 변화돼서 저장됨)
            indent=4 # 들여쓰기 간격
        )

def load_data():
    global money_data, budget # 함수 밖에 있는 변수를 사용

    try:
        with open("money.json", "r", encoding="utf-8") as file:
            data = json.load(file) # json.load(): JSON 파일을 Python 데이터로 읽음

            if isinstance(data, list): # isinstance(변수, 자료형): 이 변수가 이 자료형이 맞는지 확인 ex)isinstance(money_data, dict): money_data가 딕셔너리 타입인지 확인
                money_data = data
                budget = 30000000
            else:
                # 새로운 money.json은 딕서녀리 형식으로 저장되어 있음(budget이 추가 됐기 때문)
                budget = data.get("budget", 30000000) # data에 budget이 있으면 사용, 없으면 30000000 사용
                money_data = data.get("money_data", [])
                # get()을 사용하는 이유: key가 없는 경우 data["key"]: keyError 발생. data.get("key"): None 반환

    except FileNotFoundError:
        money_data = []

def display_data():
    for row in money_list.get_children(): # treeview 형태
        money_list.delete(row)

    for index, money in enumerate(money_data):
        money_list.insert("", "end", iid=index, values=(money['date'], money['category'], money['item'], money.get("shop", ""), f"{money['price']:,}원"))

def select_money(event=None):
    selected = money_list.selection()

    if selected:
        selected_id = selected[0] # 선택한 Treeview 행 ID

        global selected_index
        selected_index = int(selected_id)
        
        money = money_data[selected_index]

        date_entry.set_date(money["date"]) # DateEntry 방식

        category_combo.set(money["category"])

        item_entry.delete(0, tk.END)
        item_entry.insert(0, money["item"]) # entry 방식(delete & insert)

        shop_entry.set(money.get("shop", ""))

        price_entry.delete(0, tk.END)
        price_entry.insert(0, str(money["price"]))
    
def update_money():
    global selected_index

    if selected_index is None:
        messagebox.showwarning("수정 오류", "수정할 항목을 먼저 선택하세요.")
        return

    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    shop = shop_entry.get()
    price = price_entry.get()

    try:
        price = int(price.replace(",", ""))
    except:
        messagebox.showwarning("입력 오류", "금액은 숫자로 입력하세요.")
        return

    money_data[selected_index]["date"] = date
    money_data[selected_index]["category"] = category
    money_data[selected_index]["item"] = item
    money_data[selected_index]["shop"] = shop
    money_data[selected_index]["price"] = price

    save_data()
    display_data()
    update_total()

    refresh_input_entry() # 입력창 초기화
    selected_index = None # 선택 상태 초기화

def search_money():
    keyword = search_entry.get()

    # 검색어가 없으면 전체 출력
    if keyword == "":
        display_data()
        return

    money_list.delete(*money_list.get_children()) # *는 unpacking(언패킹)

    for money in money_data:
        if (keyword in money["item"] or keyword in money["category"] or keyword in money.get("shop", "")):
            money_list.insert("", "end", values=(money["date"], money["category"], money["item"], f"{money['price']:,}원"))

def show_category_state():
    category_total = {}

    for money in money_data:
        category = money["category"]
        price = money["price"]

        if category in category_total:
            category_total[category] += price
        else:
            category_total[category] = price

    result = ""
    for category, total_price in category_total.items():
        result += f"{category} : {total_price:,}원\n"

    messagebox.showinfo("카테고리별 통계", result)

def show_month_state():
    month_total = {}

    for money in money_data:
        date = money["date"]
        month = date[:7] # 앞 7글자 자르기
        price = money["price"]

        if month in month_total:
            month_total[month] += price
        else:
            month_total[month] = price

    result = ""
    for month, total_price in month_total.items():
        result += f"{month} : {total_price:,}원\n"

    messagebox.showinfo("월별 통계", result)

def show_detail_state():
    month_category_total = {}

    for money in money_data:
        date = money["date"]
        month = date[:7]
        category = money["category"]
        price = money["price"]

        if month not in month_category_total:
            month_category_total[month] = {}

        if category in month_category_total[month]:
            month_category_total[month][category] += price
        else:
            month_category_total[month][category] = price

    result = ""
    for month, categories in month_category_total.items():
        result += f"\n[{month}]\n"
        for category, total_price in categories.items():
            result += f"{category} : {total_price:,}원\n"

    messagebox.showinfo("상세 통계", result)

def show_bar_chart():
    category_total = {}

    for money in money_data:
        category = money["category"]
        price = money["price"]

        if category in category_total:
            category_total[category] += price
        else:
            category_total[category] = price

    # matplotlib은 리스트 형태를 선호함
    categories = list(category_total.keys()) # keys(): 기능 실행, keys: 기능 자체. ex)get()
    prices = list(category_total.values())

    plt.figure(figsize=(8,5))
    bars = plt.bar(categories, prices, color="#3B82F6") # 막대 그래프 생성. bar: 세로 / barh: 가로
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height/10000:.0f}만원",
            ha="center",
            va="bottom"
        )
    plt.title("📊 카테고리별 지출 현황")
    plt.xlabel("카테고리")
    plt.ylabel("금액")
    plt.tight_layout() # 여백 자동 맞춤
    plt.show() # 그래프 표시

def show_pie_chart():
    category_total = {}

    if not money_data:
        messagebox.showinfo("통계", "등록된 지출 내역이 없습니다.")
        return

    for money in money_data:
        category = money["category"]
        price = money["price"]

        if category in category_total:
            category_total[category] += price
        else:
            category_total[category] = price

    if not category_total:
        messagebox.showinfo("통계", "표시할 데이터가 없습니다.")
        return
    
    categories = list(category_total.keys())
    prices = list(category_total.values())

    max_index = prices.index(max(prices))
    explode = [0] * len(prices)
    explode[max_index] = 0.1

    plt.figure(figsize=(6,6))
    wedges, texts, autotexts = plt.pie(
        prices,
        labels=None,
        autopct=make_autopct(prices),
        startangle=90, # 기본은 3시 방향부터 시작하는데 90도를 주면 12시 방향부터 시작함
        wedgeprops={"width": 0.45}, # 도넛형 그래프
        explode=explode, # 자동으로 살짝 튀어나오게
        textprops={"fontsize": 9}
    ) # 원형 그래프 생성
    plt.legend(
        wedges,
        categories,
        title="카테고리",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    plt.title("💒 신혼 자금 사용 비율")
    plt.axis("equal") # 원형으로 맞춤
    plt.tight_layout()
    plt.show()

def make_autopct(values): # 설정값(values)을 기억하는 함수를 만들어서 반환하는 역할 (함수를 만들어서 반환하는 함수: 클로저(closure))
    def my_autopct(percent): # percent는 matplotlib가 자동으로 넣어주는 값. matplotlib이 사용할 함수
        total = sum(values)
        price = int(total * percent / 100)
        
        if percent < 5:
            return f"{percent:.1f}%"
        else:
            return f"{percent:.1f}%\n({price:,}원)"

    return my_autopct

def update_budget():
    global budget

    try:
        budget = int(budget_entry.get().replace(",", ""))
    except:
        messagebox.showwarning("입력 오류", "예산은 숫자로 입력하세요.")
        return

    save_data() 
    update_total()

def refresh_budget_entry():
    budget_entry.delete(0, tk.END)
    budget_entry.insert(0, f"{budget:,}")

def refresh_input_entry():
    date_entry.delete(0, tk.END)
    date_entry.set_date(datetime.today())
    category_combo.set("")
    item_entry.delete(0, tk.END)
    shop_entry.set("")
    price_entry.delete(0, tk.END)

def format_price(event=None):
    cursor = price_entry.index(tk.INSERT) # tk.INSERT: 현재 커서 위치
    
    # 콤마 제거
    text = price_entry.get().replace(",", "")

    # 빈칸이면 종료
    if text == "":
        return

    # 숫자가 아니면 문자 입력 취소
    if not text.isdigit():
        text = "".join(filter(str.isdigit, text)) # filter(str.isdigit, text): 숫자만 남기기 위해 사용

    # 콤마 추가
    formatted = f"{int(text):,}"

    # 커서 보정
    comma_before = price_entry.get()[:cursor].count(",")
    comma_after = formatted[:cursor].count(",")

    new_cursor = cursor + (comma_after - comma_before)

    # 다시 출력
    price_entry.delete(0, tk.END)
    price_entry.insert(0, formatted)

    # 커서 원래 위치 근처로 이동
    if new_cursor <= len(formatted):
        price_entry.icursor(new_cursor) # icursor(): Entry의 커서를 지정한 위치로 이동

def format_price2(event=None):
    # 숫자만 추출
    numbers = "".join(filter(str.isdigit, price_entry.get()))

    # 비어있으면 종료
    if not numbers:
        price_entry.delete(0, tk.END)
        return

    # 현재 숫자의 개수
    digit_pos = len("".join(filter(str.isdigit, price_entry.get()[:price_entry.index(tk.INSERT)]))) # price_entry.get()[:tk.INSERT]: 현재 커서 앞까지만 자른다. "".join(...): 다시 문자열로 만든다

    # 콤마 추가
    formatted = f"{int(numbers):,}"

    # 다시 출력
    price_entry.delete(0, tk.END)
    price_entry.insert(0, formatted)

    # 숫자 개수를 기준으로 커서 위치 계산
    count = 0
    cursor = len(formatted)

    for idx, char in enumerate(formatted):
        if char.isdigit():
            count += 1

        if count == digit_pos:
            cursor = idx + 1
            break

    price_entry.icursor(cursor)

def sort_price():
    global price_reverse

    # 오름차순이면 내림차순(reverse=True)으로 정렬 / 내림차순이면 오름차순(reverse=False)으로 정렬
    money_data.sort(key=lambda money: money["price"], reverse=price_reverse) # money_data를 금액 기준으로 정렬. money: money["price"]에서 money는 내가 지정한 변수명. 다른걸로 바꿔도 상관없음
    price_reverse = not price_reverse

    display_data()

def sort_column(column):
    # 오름차순이면 내림차순(reverse=True)으로 정렬 / 내림차순이면 오름차순(reverse=False)으로 정렬
    money_data.sort(key=lambda money: money[column], reverse=sort_reverse[column])

    sort_reverse[column] = not sort_reverse[column] # 새 딕셔너리 통째로 바꾸는게 아니니까 global 사용 안

    display_data()


# ==========================================
# 실행
# ==========================================
price_entry.bind("<KeyRelease>", format_price2)

load_data()
display_data()
update_total()
refresh_budget_entry()

window.mainloop() # 이벤트 루프 시작(창이 종료될 때까지 프로그램 실행)