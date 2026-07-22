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

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

money_data = []
selected_index = None

# 메인 윈도우(창) 생성
window = tk.Tk() 

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

    money_list.insert(tk.END, f"{date} | {category} | {item} | {price}원") # tk.END: 맨 마지막 위치에 추가
    # f"문자열 {변수:포맷} 문자열"
    # ex) 소수점 f"{price:.2f}" / 퍼센트 f"{rate:.0%}"

    money_data.append({
        "date": date,
        "category": category,
        "item": item,
        "price": price
    }) # Python의 dictionary(딕셔너리)

    update_total()

    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

    save_data()

def update_total():
    total = 0

    for money in money_data:
        # total += int(money["price"]) try/except 문으로 숫자 검증했으니까 바로 저장 가능
        total += money["price"]

    total_label.config(text=f"총 지출 : {total:,}원") # config: 이미 만들어진 위젯의 설정 변경

def delete_money():
    selected = money_list.curselection() # 선택한 위치 가져오기

    if not selected:
        messagebox.showwarning(
            "삭제 오류",
            "삭제할 항목을 선택하세요."
        )
    
        return
    
    if selected:
        index = selected[0]

        money_data.pop(index)
        money_list.delete(index)

        save_data()
        update_total()

def save_data():
    # with: 열고 → 사용하고 → 자동 정리
    with open("money.json", "w", encoding="utf-8") as file: # open(): money.json 파일을 쓰기 모드로 열어줘 (w:새로 쓰기, r:읽기, a:이어 쓰기), as file: 열린 파일을 file이라는 이름으로 사용
        json.dump( # json.dump(): Python 데이터를 JSON 파일로 저장
            money_data,
            file,
            ensure_ascii=False, # 한글을 그대로 저장(true로 하면 유니코드로 변화돼서 저장됨)
            indent=4
        )

def load_data():
    global money_data # 함수 밖에 있는 money_data를 사용할 거야

    try:
        with open(
            "money.json",
            "r",
            encoding="utf-8"
        ) as file:

            money_data = json.load(file) #json.load(): JSON 파일을 Python 데이터로 읽음

    except FileNotFoundError:
        money_data = []

def display_data():
    money_list.delete(0, tk.END)

    for money in money_data:
        money_list.insert(
            tk.END,
            f"{money['date']} | {money['category']} | {money['item']} | {money['price']:,}원"
        )

def select_money(event=None):
    selected = money_list.curselection()
    
    if not selected:
        messagebox.showwarning(
            "수정 오류",
            "수정할 항목을 선택하세요."
        )

        return

    if selected:
        index = selected[0]

        global selected_index
        selected_index = index

        money = money_data[index]

        date_entry.delete(0, tk.END)
        date_entry.insert(0, money["date"])

        category_combo.set(money["category"])

        item_entry.delete(0, tk.END)
        item_entry.insert(0, money["item"])

        price_entry.delete(0, tk.END)
        price_entry.insert(0, money["price"])
    
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

    money_data[selected_index] = {
        "date": date,
        "category": category,
        "item": item,
        "price": price
    }

    save_data()
    display_data()
    update_total()

def search_money():
    keyword = search_entry.get()

    if keyword == "":
        display_data()
        
        return
    
    money_list.delete(0, tk.END)

    for money in money_data:
        if keyword in money["item"] or keyword in money["category"]:
            money_list.insert(
                tk.END,
                f"{money['date']} | {money['category']} | {money['item']} | {money['price']:,}원"
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

def show_graph():
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

    plt.bar(categories, prices) # 막대 그래프 생성
    plt.title("카테고리별 지출")
    plt.xlabel("카테고리")
    plt.ylabel("금액")
    plt.show() # 그래프 표시

def show_pie_graph():
    category_total = {}

    for money in money_data:
        category = money["category"]
        price = money["price"]

        if category in category_total:
            category_total[category] += price

        else:
            category_total[category] = price

    categories = list(category_total.keys())
    prices = list(category_total.values())

    plt.pie(prices, labels=categories, autopct="%1.1f%%") # 원형 그래프 생성
    plt.title("카테고리별 지출 비율")
    plt.show()

# =====================
# 화면 영역
# =====================
# 창 설정
window.title("💒 신혼 자금 관리") # 창 제목
window.geometry("800x600") # 창 크기 (widthxheight)

# 창 꾸미기?
# Entry → 사용자가 입력하는 곳
# Button → 사용자가 누르는 곳
# Label → 정보를 보여주는 곳
date_label = tk.Label(window, text="날짜") # tk.Label(넣을_창, 표시할_글자)
date_label.grid(row=0, column=0)
# 1. pack() : 자동 배치
# 2. grid() : 행(row), 열(column) 기준 배치
# 3. place() : 좌표(x, y) 기준 배치
date_entry = DateEntry(window, width=12, date_pattern="yyyy-mm-dd")
date_entry.grid(row=0, column=1)

category_label = tk.Label(window, text="카테고리")
category_label.grid(row=1, column=0)

category_combo = ttk.Combobox(window, values=["가구","가전","생활용품","여행"], state="readonly")
category_combo.grid(row=1, column=1)

item_label = tk.Label(window, text="항목") 
item_label.grid(row=2, column=0)

item_entry = tk.Entry(window)
item_entry.grid(row=2, column=1)

price_label = tk.Label(window, text="금액")
price_label.grid(row=3, column=0)

price_entry = tk.Entry(window, width=20)
price_entry.grid(row=3, column=1)

add_button = tk.Button(window, text="추가", command=add_money) # command=add_money() 프로그램 시작할 때 바로 실행
add_button.grid(row=4, column=0)

# select_button = tk.Button(window, text="수정 선택", command=select_money)
# select_button.grid(row=4, column=1)

update_button = tk.Button(window, text="수정", command=update_money)
update_button.grid(row=4, column=1)

delete_button = tk.Button(window, text="삭제", command=delete_money)
delete_button.grid(row=4, column=2)

search_entry = tk.Entry(window)
search_entry.grid(row=5, column=0)

search_button = tk.Button(window, text="검색", command=search_money)
search_button.grid(row=5, column=1)

money_list = tk.Listbox(window, width=50)
money_list.bind("<<ListboxSelect>>", select_money)
money_list.grid(row=6, column=0, columnspan=2)

total_label = tk.Label(window, text="총 지출 : 0원")
total_label.grid(row=7, column=0, columnspan=2)

category_stats_button = tk.Button(window, text="통계", command=show_category_state)
category_stats_button.grid(row=8, column=0)

month_stats_button = tk.Button(window, text="월별 통계", command=show_month_state)
month_stats_button.grid(row=8, column=1)

detail_stats_button = tk.Button(window, text="상세 통계", command=show_detail_state)
detail_stats_button.grid(row=8, column=2)

graph_button = tk.Button(window, text="그래프", command=show_graph)
graph_button.grid(row=9, column=0)

pie_button = tk.Button(window, text="비율 그래프", command=show_pie_graph)
pie_button.grid(row=9, column=1)

# =====================
# 실행
# =====================
# 프로그램 실행
load_data()
display_data()
update_total()

window.mainloop() # 이벤트 루프 시작(창이 종료될 때까지 프로그램 실행)
