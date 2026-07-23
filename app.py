# GUI를 만들기 위한 tkinter 라이브러리 불러오기
import tkinter as tk
# tkinter 안에 있는 messagebox 기능 가져와줘
from tkinter import messagebox

import json

from datetime import datetime
from tkcalendar import DateEntry
from tkinter import ttk

# 그래프를 만들기 위한 matplotlib 라이브러리 불러오기 (pyplot: 그래프 그리는 기능)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "Malgun Gothic" # or plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

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

# 메인 윈도우(창) 생성
window = tk.Tk()

# =====================
# 화면 큰 구조
# =====================
title_frame = tk.Frame(window)
title_frame.grid(
    row=0,
    column=0,
    pady=10
)

top_frame = tk.Frame(window)
top_frame.grid(
    row=1,
    column=0,
    padx=20,
    pady=10
)
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)

bottom_frame = tk.Frame(window)
bottom_frame.grid(
    row=2,
    column=0,
    padx=20,
    pady=10
)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

title_label = tk.Label(
    title_frame,
    # text="💰 신혼 가계부",
    font=("맑은 고딕", 10, "bold")
)

title_label.pack()

# 창 설정
window.title("💒 신혼 자금 관리") # 창 제목
window.geometry("820x900") # 창 크기 (widthxheight)

# =====================
# 화면 영역 Frame 분리
# =====================
dashboard_frame = tk.Frame(bottom_frame)
dashboard_frame.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=20,
    pady=20
)

# 대시보드 카드 --
budget_card = tk.Label(
    dashboard_frame,
    text=f"💰 예산\n\n{budget:,}원",
    font=("맑은 고딕", 10, "bold"),
    width=18,
    height=5,
    relief="groove", # solid: 실선, groove: 홈이 파인 듯한 이중 테두리
    bg="#E8F5E9"
)
budget_card.grid(row=0, column=0, pady=10) # pady: 위아래 여백

used_card = tk.Label(
    dashboard_frame,
    text="💸 현재 지출\n\n0원",
    font=("맑은 고딕", 10, "bold"),
    width=18,
    height=5,
    relief="groove",
    bg="#FFF3E0"
)
used_card.grid(row=0, column=1, pady=10)

remain_card = tk.Label(
    dashboard_frame,
    text=f"💵 남은 금액\n\n{budget:,}원",
    font=("맑은 고딕", 10, "bold"),
    width=18,
    height=5,
    relief="groove",
    bg="#E3F2FD"
)
remain_card.grid(row=0, column=2, pady=10)
# -- 대시보드 카드

budget_frame = tk.Frame(top_frame)
budget_frame.grid(
    row=0,
    column=1,
    columnspan=2,
    pady=10
)

input_frame = tk.Frame(top_frame)
input_frame.grid(
    row=0,
    column=0,
    padx=20,
    pady=20
)

list_frame = tk.Frame(bottom_frame)
list_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    padx=20,
    pady=20,
    sticky="nsew"
)
list_frame.grid_columnconfigure(0, weight=1) # list_frame의 0번째 컬럼은 남는 공간이 있으면 늘어나라
list_frame.grid_columnconfigure(1, weight=0) # list_frame의 1번째 컬럼은 남는 공간을 받지 마라
# column 0(Treeview) → 남은 공간 차지 / column 1(scrollbar) → 고정 크기
list_frame.grid_rowconfigure(0, weight=0)
list_frame.grid_rowconfigure(1, weight=1) # grid_rowconfigure()의 숫자는 list_frame 내부의 row 번호. 즉, money_list의 row가 1이면 매칭 됨

search_frame = tk.Frame(list_frame)
search_frame.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="ew"
)
search_frame.grid_columnconfigure(0, weight=1)
search_frame.grid_columnconfigure(1, weight=0)

button_frame = tk.Frame(list_frame)
button_frame.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="ew"
)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# =====================
# 함수 영역
# =====================
def add_money():
    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    price = price_entry.get()

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    if item == "" or price == "":
        messagebox.showwarning("입력 오류", "항목과 금액을 입력하세요.")
        return

    try:
        price = int(price)
    except:
        messagebox.showwarning("입력 오류", "금액은 숫자로 입력하세요.")
        return

    # listbox 형태
    # money_list.insert(tk.END, f"{date} | {category} | {item} | {price}원") # Listbox형태. tk.END: 맨 마지막 위치에 추가
    # f"문자열 {변수:포맷} 문자열"
    # ex) 소수점 f"{price:.2f}" / 퍼센트 f"{rate:.0%}"

    # Treeview 형태. 화면(Treeview)에 직접 추가
    # money_list.insert("", "end", values=(date, category, item, f"{price:,}원"))
    # 주석한 이유 - display_data() 호출을 하기 때문. 여기서 money_list에 insert 함

    # 실제 데이터 추가
    money_data.append({
        "date": date,
        "category": category,
        "item": item,
        "price": price
    }) # Python의 dictionary(딕셔너리)

    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    
    save_data()
    display_data()
    update_total()

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

    budget_card.config(text=f"💰 예산\n\n{budget:,}원")
    used_card.config(text=f"💸 현재 지출\n\n{total:,}원\n사용률 {rate:.1f}%")
    remain_card.config(text=f"💵 남은 금액\n\n{remain:,}원")

def delete_money():
    # selected = money_list.curselection() # Listbox형태. 선택한 위치 가져오기
    selected = money_list.selection()

    if not selected:
        messagebox.showwarning(
            "삭제 오류",
            "삭제할 항목을 선택하세요."
        )
    
        return
    
    if selected:
        # index = selected[0]
        # money_data.pop(index)
        # money_list.delete(index)
        
        result = messagebox.askyesno(
            "삭제 확인",
            "정말 삭제하시겠습니까?"
        )

        if not result:
            return

        selected_id = selected[0]
        index = int(selected_id)

        money_data.pop(index) # 실제 데이터 삭제
        money_list.delete(selected_id) # Treeview 화면에서 삭제

        save_data()
        display_data() # 삭제 후 인덱스 재배치
        update_total()

        # 입력창 초기화
        refresh_input_entry()

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
            indent=4
        )

def load_data():
    global money_data, budget # 함수 밖에 있는 변수를 사용

    try:
        with open("money.json", "r", encoding="utf-8") as file:
            data = json.load(file) #json.load(): JSON 파일을 Python 데이터로 읽음

            if isinstance(data, list): # isinstance(변수, 자료형): 이 변수가 이 자료형이 맞는지 확인 ex)isinstance(money_data, dict): money_data가 딕셔너리 타입인지 확인
                # 기존 money.json은 리스트 형식으로 저장되어 있음
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
    # money_list.delete(0, tk.END) # listbox 형태

    for row in money_list.get_children(): #treeview 형태
        money_list.delete(row)

    # for money in money_data:
    #     # money_list.insert(tk.END, f"{money['date']} | {money['category']} | {money['item']} | {money['price']:,}원")
    #     money_list.insert("", "end", values=(money['date'], money['category'], money['item'], f"{money['price']:,}원")) # 이게 Treeview 형태

    for index, money in enumerate(money_data):
        money_list.insert("", "end", iid=index, values=(money['date'], money['category'], money['item'], f"{money['price']:,}원")) # 이게 Treeview 형태

def select_money(event=None):
    # selected = money_list.curselection() # 이거는 Listbox전용. Treeview에서는 사용 불가
    selected = money_list.selection()

    if selected:
        # index = selected[0]

        selected_id = selected[0] # 선택한 Treeview 행 ID

        global selected_index
        selected_index = int(selected_id)
        
        money = money_data[selected_index]

        # date_entry.delete(0, tk.END)
        # date_entry.insert(0, money["date"]) # entry 방식(delete & insert)
        date_entry.set_date(money["date"]) # DateEntry 방식

        category_combo.set(money["category"])

        item_entry.delete(0, tk.END)
        item_entry.insert(0, money["item"])

        price_entry.delete(0, tk.END)
        price_entry.insert(0, str(money["price"]))
    
def update_money():
    global selected_index

    if selected_index is None:
        messagebox.showwarning(
            "수정 오류",
            "수정할 항목을 먼저 선택하세요."
        )

        return

    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    price = price_entry.get()

    try:
        price = int(price)
    except:
        messagebox.showwarning(
            "입력 오류",
            "금액은 숫자로 입력하세요."
        )

        return

    money_data[selected_index]["date"] = date
    money_data[selected_index]["category"] = category
    money_data[selected_index]["item"] = item
    money_data[selected_index]["price"] = price

    save_data()
    display_data()
    update_total()

    # 입력창 초기화
    refresh_input_entry()

    # 선택 상태 초기화
    selected_index = None

def search_money():
    keyword = search_entry.get()

    # 검색어가 없으면 전체 출력
    if keyword == "":
        display_data()
        
        return
    
    # money_list.delete(0, tk.END)

    # for money in money_data:
    #     if keyword in money["item"] or keyword in money["category"]:
    #         money_list.insert(
    #             tk.END,
    #             f"{money['date']} | {money['category']} | {money['item']} | {money['price']:,}원"
    #         )

    money_list.delete(*money_list.get_children()) # *는 unpacking(언패킹)

    for money in money_data:
        if keyword in money["item"] or keyword in money["category"]:
            money_list.insert(
                "",
                "end",
                values=(
                    money["date"],
                    money["category"],
                    money["item"],
                    f"{money['price']:,}원"
                )
            )

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
    bars = plt.bar(categories, prices) # 막대 그래프 생성. bar: 세로 / barh: 가로
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
        messagebox.showinfo(
            "통계",
            "등록된 지출 내역이 없습니다."
        )

        return

    for money in money_data:
        category = money["category"]
        price = money["price"]

        if category in category_total:
            category_total[category] += price

        else:
            category_total[category] = price

    if not category_total:
        messagebox.showinfo(
            "통계",
            "표시할 데이터가 없습니다."
        )

        return
    
    categories = list(category_total.keys())
    prices = list(category_total.values())

    max_index = prices.index(max(prices))
    explode = [0] * len(prices)
    explode[max_index] = 0.1

    plt.figure(figsize=(6,6))
    wedges, texts, autotexts = plt.pie(
        prices,
        # labels=categories,
        labels=None,
        # autopct="%1.1f%%",
        autopct=make_autopct(prices),
        startangle=90, # 기본은 3시 방향부터 시작하는데 90도를 주면 12시 방향부터 시작함
        # shadow=True,
        wedgeprops={"width": 0.45}, # 도넛
        explode=explode, # 자동으로 살짝 튀어나오게
        textprops={"fontsize": 9}
        # labeldistance=1.15
        # pctdistance=0.6
    )# 원형 그래프 생성
    plt.legend(
        wedges,
        categories,
        title="카테고리",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    plt.title("💒 신혼 자금 사용 비율")
    plt.axis("equal") # 원으로
    plt.tight_layout() # 여백 자동 맞춤
    plt.show()

def make_autopct(values): # 설정값(values)을 기억하는 함수를 만들어서 반환하는 역할

    def my_autopct(percent): # percent는 matplotlib가 자동으로 넣어주는 값
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
        messagebox.showwarning(
            "입력 오류",
            "예산은 숫자로 입력하세요."
        )
        
        return

    save_data() 
    update_total()

def refresh_budget_entry():
    budget_entry.delete(0, tk.END)
    budget_entry.insert(0, f"{budget:,}")

def refresh_input_entry():
    # 입력창 초기화
    date_entry.delete(0, tk.END)
    date_entry.set_date(datetime.today())
    category_combo.set("")
    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def sort_price():
    global price_reverse

    # 오름차순이면 내림차순(reverse=True)으로 정렬 / 내림차순이면 오름차순(reverse=False)으로 정렬
    money_data.sort(key=lambda money: money["price"], reverse=price_reverse) # money_data를 금액 기준으로 정렬. money: money["price"]에서 money는 내가 지정한 변수명. 다른걸로 바꿔도 상관없음

    price_reverse = not price_reverse

    display_data()

def sort_column(column):
    # 오름차순이면 내림차순(reverse=True)으로 정렬 / 내림차순이면 오름차순(reverse=False)으로 정렬
    money_data.sort(key=lambda money: money[column], reverse=sort_reverse[column])

    sort_reverse[column] = not sort_reverse[column] # 새 딕셔너리 통째로 바꾸는게 아니니까 global 사용 안함

    display_data()


# =====================
# 화면 영역
# =====================
# 창 꾸미기
entry_style = {
    "font": ("맑은 고딕", 11),
    "width": 30,
    "relief": "flat",
    "bd": 1
}

button_font = ("맑은 고딕", 10, "bold")
normal_button = {
    "font": button_font,
    "width": 15,
    "height": 2,
    "relief": "flat", # 입체 버튼 효과 제거
    "bd": 0, # 테두리 제거
    "cursor": "hand2",
    "fg": "white", # 글자 색
    "activeforeground": "white" # 클릭할 때 글자색
}

stat_button = {
    **normal_button,
    "bg": "#4F81BD", # 기본 버튼 색
    "activebackground": "#3B6A9E" # 클릭할 때 색
}

insert_button = {
    **normal_button,
    "bg": "#70AD47",
    "activebackground": "#649A40"
}

update_button = {
    **normal_button,
    "bg": "#ED7D31",
    "activebackground": "#DD742E"
}

delete_button = {
    **normal_button,
    "bg": "#C00000",
    "activebackground": "#900000"
}

search_button = {
    **normal_button,
    "height": 1,
    "bg": "#4F81BD", # 기본 버튼 색
    "activebackground": "#3B6A9E" # 클릭할 때 색
}

# Entry → 사용자가 입력하는 곳
# Button → 사용자가 누르는 곳
# Label → 정보를 보여주는 곳
budget_label = tk.Label(budget_frame, text="예산")
budget_label.grid(row=0, column=0, padx=5) # padx: 위젯 바깥쪽의 가로(좌우) 여백 / ipadx: 위젯 안쪽의 좌우 여백(위젯 자체의 너비를 늘림) / pady: 위젯 바깥쪽의 세로(상하) 여백

budget_entry = tk.Entry(budget_frame, width=20)
budget_entry.grid(row=0, column=1)

budget_button = tk.Button(budget_frame, text="적용", command=update_budget)
budget_button.grid(row=0, column=2, padx=5)

date_label = tk.Label(input_frame, text="날짜") # tk.Label(넣을_창, 표시할_글자)
date_label.grid(row=0, column=0)
# 1. pack() : 자동 배치
# 2. grid() : 행(row), 열(column) 기준 배치
# 3. place() : 좌표(x, y) 기준 배치
date_entry = DateEntry(input_frame, date_pattern="yyyy-mm-dd", **entry_style)
date_entry.grid(row=0, column=1)

category_label = tk.Label(input_frame, text="분류")
category_label.grid(row=1, column=0)

style = ttk.Style()
style.configure(
    "Custom.TCombobox",
    font=("맑은 고딕", 11),
    padding=5
)
category_combo = ttk.Combobox(input_frame, values=["가구","가전","생활용품","여행"], state="readonly", style="Custom.TCombobox")
category_combo.grid(row=1, column=1)

item_label = tk.Label(input_frame, text="항목") 
item_label.grid(row=2, column=0)

item_entry = tk.Entry(input_frame, **entry_style)
item_entry.grid(row=2, column=1)

price_label = tk.Label(input_frame, text="금액")
price_label.grid(row=3, column=0)

price_entry = tk.Entry(input_frame, **entry_style)
price_entry.grid(row=3, column=1)

add_button = tk.Button(input_frame, text="➕ 추가", command=add_money, **insert_button) # command=add_money() 프로그램 시작할 때 바로 실행
add_button.grid(row=4, column=0)

# select_button = tk.Button(window, text="수정 선택", command=select_money)
# select_button.grid(row=4, column=1)

update_button = tk.Button(input_frame, text="✏ 수정", command=update_money, **update_button)
update_button.grid(row=4, column=1)

delete_button = tk.Button(input_frame, text="🗑 삭제", command=delete_money, **delete_button)
delete_button.grid(row=4, column=2)

search_entry = tk.Entry(search_frame, **entry_style)
search_entry.grid(row=0, column=0, sticky="ew")

search_button = tk.Button(search_frame, text="🔍 검색", command=search_money, **search_button)
search_button.grid(row=0, column=1, pady=5)

# listbox
# money_list = tk.Listbox(list_frame, width=50)
# money_list.bind("<<ListboxSelect>>", select_money)
# money_list.grid(row=6, column=0, columnspan=2)

# treeview
style = ttk.Style()
style.configure("Treeview", font=("맑은 고딕", 10), rowheight=30)
style.configure("Treeview.Heading", font=("맑은 고딕", 11, "bold"))
style.map(
    "Treeview",
    background=[
        ("selected", "#AED6F1")
    ],
    foreground=[
        ("selected", "black")
    ]
)
money_list = ttk.Treeview(list_frame, columns=("date", "category", "item", "price"), show="headings", height=10)
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=money_list.yview) # money_list.yview: Treeview → Scrollbar. 스크롤바 움직이면 Treeview의 세로 위치를 바꿔라
money_list.configure(yscrollcommand=scrollbar.set) # scrollbar.set: Scrollbar → Treeview. Treeview가 현재 위치를 스크롤바에 알려줘라
money_list.heading("date", text="날짜", command=lambda: sort_column("date")) # lambda 사용하는 이유: 클릭했을 때 실행하라는 의미. command=sort_column("date") 이렇게 쓰면 프로그램 시작할 때 바로 실행
money_list.heading("category", text="분류", command=lambda: sort_column("category"))
money_list.heading("item", text="항목", command=lambda: sort_column("item"))
money_list.heading("price", text="금액", command=lambda: sort_column("price"))
money_list.column("date", width=120, anchor="center")
money_list.column("category", width=100, anchor="center")
money_list.column("item", width=200, anchor="w", stretch=True)
money_list.column("price", width=120, anchor="e")
money_list.bind("<<TreeviewSelect>>", select_money)
money_list.grid(row=1, column=0, sticky="nsew") #sticky: 위젯을 셀의 어느 방향으로 붙일지 정하는 옵션. n(north), s(south), e(east), w(west)
# nsew: 위,아래,왼,오 모든 방향으로 붙으라는거니까 커진 grid 칸 안에서 Treeview도 같이 늘어나라는 뜻
scrollbar.grid(row=1, column=1, sticky="ns")

total_label = tk.Label(list_frame, text="총 지출 : 0원")
total_label.grid(row=2, column=0, columnspan=2)

# category_stats_button = tk.Button(window, text="통계", command=show_category_state)
# category_stats_button.grid(row=8, column=0)

# month_stats_button = tk.Button(window, text="월별 통계", command=show_month_state)
# month_stats_button.grid(row=8, column=1)

# detail_stats_button = tk.Button(window, text="상세 통계", command=show_detail_state)
# detail_stats_button.grid(row=8, column=2)

bar_button = tk.Button(button_frame, text="📈 지출 비교", command=show_bar_chart, **stat_button)
bar_button.grid(row=0, column=0, padx=20, pady=20)

pie_button = tk.Button(button_frame, text="📊 카테고리 비율", command=show_pie_chart, **stat_button)
pie_button.grid(row=0, column=1, padx=20, pady=20)

# =====================
# 실행
# =====================
# 프로그램 실행
load_data()
display_data()
update_total()

refresh_budget_entry()

window.mainloop() # 이벤트 루프 시작(창이 종료될 때까지 프로그램 실행)
