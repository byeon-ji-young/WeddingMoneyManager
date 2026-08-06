import tkinter as tk # GUI를 만들기 위한 tkinter 라이브러리 불러오기
from tkinter import messagebox, ttk # tkinter 안에 있는 messagebox, ttk 기능 가져와줘

# [★팝업 창 분리] 팝업 창 모듈 불러오기
from expense_dialog import ExpenseDialog
from excel_export import excel_export_file
from csv_export import csv_export_file
from statistics_window import StatisticsWindow
from database_backup import backup_database, restore_database

import database

# ==========================================
# 1. 전역 변수 및 데이터 설정
# ==========================================
money_data = [] # 화면 표시용 캐시
selected_index = None
budget = 30000000
remain = 0
price_reverse = False
sort_reverse = {
    "date": False,
    "category": False,
    "item": False,
    "shop": False,
    "price": False,
    "payment": False
}
progress_value = 0

# ==========================================
# 2. 메인 윈도우(창) 생성
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
# 3. 로직 및 이벤트 처리 함수 정의
# ==========================================
# 지출 항목 추가 (팝업 연동)
def open_add_dialog():
    # 팝업 창 띄우기
    dialog = ExpenseDialog(window, title="지출 추가")
    # 사용자가 팝업에서 [저장]이나 [취소]를 누르고 창을 닫을 때까지 메인 코드 대기
    window.wait_window(dialog)

    # 팝업이 닫힌 후, 저장된 결과값이 있으면 리스트에 추가
    if dialog.result:
        # SQLite 추가
        new_id = database.add_expense(dialog.result)

        # DB에서 다시 불러오기
        global money_data
        money_data = database.get_all_expenses()

        # 화면 갱신
        display_data()
        update_total()

        # 추가한 항목 자동 선택
        # new_id = money_data[-1]["id"]
        money_list.selection_set(new_id ) # 해당 행 선택
        money_list.focus(new_id ) # Treeview 내부 커서 이동
        money_list.see(new_id ) # 해당 행이 안 보이면 자동 스크롤

# 선택 항목 수정 (팝업 연동)
def open_edit_dialog():
    global money_data # 새로운 리스트를 대입하는 거라 global 필요

    selected = money_list.selection()

    if not selected:
        messagebox.showwarning("수정 오류", "수정할 항목을 먼저 선택하세요.")
        return

    selected_id = int(selected[0]) # 선택한 Treeview 행 iid
    selected_data = None

    for money in money_data:
        if money["id"] == selected_id:
            selected_data = money
            break

    if selected_data is None:
        messagebox.showwarning("오류", "데이터를 찾을 수 없습니다.")
        return
    
    # 팝업 창 띄우기
    dialog = ExpenseDialog(window, title="지출 수정", initial_data=selected_data)
    # 사용자가 팝업에서 [저장]이나 [취소]를 누르고 창을 닫을 때까지 메인 코드 대기
    window.wait_window(dialog)

    # 팝업이 닫힌 후, 저장된 결과값이 있으면 리스트에 추가
    if dialog.result:
        # SQLite 수정
        database.update_expense(selected_id, dialog.result)

        # DB에서 다시 불러오기
        money_data = database.get_all_expenses()

        # 화면 갱신
        display_data()
        update_total()

        # 수정한 항목 다시 선택
        money_list.selection_set(str(selected_id)) # 해당 행 선택
        money_list.focus(str(selected_id)) # Treeview 내부 커서 이동
        money_list.see(str(selected_id)) # 해당 행이 안 보이면 자동 스크롤
        # str() 적은 이유: Treeview의 iid는 문자열로 관리

# 선택 항목 삭제
def delete_money():
    global money_data # 새로운 리스트를 대입하는 거라 global 필요

    selected = money_list.selection()

    if not selected:
        messagebox.showwarning("삭제 오류", "삭제할 항목을 선택하세요.")
        return
    
    result = messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?")

    if not result:
        return

    selected_id = int(selected[0]) # 선택한 Treeview 행 iid

    # SQLite 삭제
    database.delete_expense(selected_id)

    # DB 다시 불러오기
    money_data = database.get_all_expenses()

    # 화면 갱신
    display_data()
    update_total()

# 예산 프로그래스 바 애니메이션
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

# 합계 및 예산 현황 업데이트
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
    # used_value.config(text=f"{total:,}원\n({rate:.1f}%)")
    used_value.config(text=f"{total:,}원 ({rate:.1f}%)")
    remain_value.config(text=f"{remain:,}원")

    # Progressbar
    progress["value"] = min(rate, 100)

    if remain < 0:
        remain_value.config(fg="#E11D48")
    else:
        remain_value.config(fg="#0F766E")

    # 상태 표시
    if rate < 70:
        progress.configure(style="Green.Horizontal.TProgressbar")
        progress_status.config(text=f"✅ 예산의 {rate:.1f}%를 사용했습니다.", fg="#0F766E")

    elif rate < 100:
        progress.configure(style="Orange.Horizontal.TProgressbar")
        progress_status.config(text=f"⚠ 예산의 {rate:.1f}%를 사용했습니다.", fg="#EA580C")

    else:
        progress.configure(style="Red.Horizontal.TProgressbar")
        over = total - budget
        progress_status.config(text=f"🚨 예산을 {over:,}원 초과했습니다.", fg="#E11D48")

    animate_progress(rate)

# 데이터 불러오기
def load_data():
    global money_data, budget # 함수 밖에 있는 변수를 사용

    money_data = database.get_all_expenses()
    budget = int(database.get_setting("budget") or 0) # settings 테이블에 budget 값이 없으면 기본값 0 사용

# 목록 새로고침
def display_data():
    # 기존 목록 삭제
    # for row in money_list.get_children(): # treeview 형태
    #     money_list.delete(row)
    money_list.delete(*money_list.get_children())

    # 데이터가 없으면 안내 메시지 표시
    if not money_data:
        # money_list.insert("", "end", values=("", "", "등록된 지출 내역이 없습니다.", "", "", ""))
        no_data_label.place(relx=0.5, rely=0.4, anchor="center") # 표 한가운데 안내 문구 띄우기 (relx=0.5, rely=0.4 는 중앙 위치)
        return
    else:
        no_data_label.place_forget() # 데이터가 있으면 안내 문구 숨기기

    # 데이터가 있으면 정상 출력
    for money in money_data:
        money_list.insert("", "end", iid=money['id'], values=(money['date'], money['category'], money['item'], money.get("shop", ""), f"{money['price']:,}원", money.get("payment", "")))

    search_count_label.config(text=f"총 {len(money_data)}건")

# 검색 및 필터링 기능
def search_money():
    keyword = search_entry.get().strip() # strip: 앞 뒤 공백 제거
    if keyword == "🔍 검색어 입력...":
        keyword = ""

    category = category_filter.get()
    payment = payment_filter.get()

    # 검색어가 없으면 전체 출력
    if keyword == "" and category == "전체" and payment == "전체":
        display_data()
        return

    # 전체 선택이면 조건 제거
    if category == "전체":
        category = ""

    if payment == "전체":
        payment = ""

    money_list.delete(*money_list.get_children()) # *는 unpacking(언패킹)

    results = database.get_expenses(keyword, category, payment)
    
    for money in results:
        money_list.insert("", "end", iid=money["id"], values=(money["date"], money["category"], money["item"], money.get("shop", ""), f"{money['price']:,}원", money.get("payment", "")))

    # 검색 결과 없음
    if len(results) == 0:
        no_data_label.place(relx=0.5, rely=0.4, anchor="center") # 표 한가운데 안내 문구 띄우기 (relx=0.5, rely=0.4 는 중앙 위치)
    else:
        no_data_label.place_forget() # 데이터가 있으면 안내 문구 숨기기

    search_count_label.config(text=f"총 {len(results)}건")

# 검색 조건 초기화
def reset_search():
     # 검색어 초기화
    search_entry.delete(0, tk.END)
    search_entry.insert(0, "🔍 검색어 입력...")
    search_entry.config(fg="#94A3B8")

    # 필터 초기화
    category_filter.set("전체")
    payment_filter.set("전체")

    # 전체 목록 다시 표시
    display_data()

# 예산 설정 변경
def update_budget():
    global budget

    try:
        budget = int(budget_entry.get().replace(",", ""))
    except:
        messagebox.showwarning("입력 오류", "예산은 숫자로 입력하세요.")
        return

    database.update_setting("budget", str(budget))

    update_total()

# 예산 입력 초기화
def refresh_budget_entry():
    budget_entry.delete(0, tk.END)
    budget_entry.insert(0, f"{budget:,}")

# 테이블 칼럼 정렬 (오름차순/내림차순 토글)
def sort_column(column):
    # 오름차순이면 내림차순(reverse=True)으로 정렬 / 내림차순이면 오름차순(reverse=False)으로 정렬
    money_data.sort(key=lambda money: money.get(column, ""), reverse=sort_reverse[column]) # money_data를 금액 기준으로 정렬. money: money["price"]에서 money는 내가 지정한 변수명. 다른걸로 바꿔도 상관없음

    sort_reverse[column] = not sort_reverse[column] # 새 딕셔너리 통째로 바꾸는게 아니니까 global 사용 안함

    display_data()

# 엑셀 생성
def excel_export():
    excel_export_file(money_data, budget)

    # messagebox.showinfo("완료", "엑셀 파일이 저장되었습니다.")

# 통계 팝업 생성
def open_statistics():
    if not money_data:
        messagebox.showwarning(
            "데이터 없음",
            "지출 데이터가 없습니다."
        )
        return

    StatisticsWindow(window, money_data)

# ==========================================
# 4. 상단 타이틀 및 예산 설정 영역
# ==========================================
# 1. pack() : 자동 배치
# 2. grid() : 행(row), 열(column) 기준 배치
# 3. place() : 좌표(x, y) 기준 배치
header_frame = tk.Frame(window, bg="#F4F6F9")
header_frame.pack(fill="x", padx=30, pady=(20, 10)) # fill="x" : 가로 방향으로 부모 크기에 맞게 늘어남 / "y" : 세로 방향으로 늘어남 / "both" : 가로와 세로 모두 늘어남
# padx: 위젯 바깥쪽의 가로(좌우) 여백 / ipadx: 위젯 안쪽의 좌우 여백(위젯 자체의 너비를 늘림) / pady: 위젯 바깥쪽의 세로(상하) 여백

title_label = tk.Label(
    header_frame,
    text="💍 결혼 준비 비용 관리",
    font=("맑은 고딕", 16, "bold"),
    bg="#F4F6F9",
    fg="#1E293B"
)
# title_label.pack(side="left") # "left" : 왼쪽부터 배치 / "right" : 오른쪽부터 배치 / "top" : 위쪽부터 배치(기본값) / "bottom" : 아래쪽부터 배치
title_label.pack(anchor="w", pady=(0, 15))

# 예산 입력 프레임
budget_frame = tk.Frame(header_frame, bg="#F4F6F9")
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
# 5. 대시보드 카드 영역(Dashboard Summary Cards): 총 예산 / 현재 지출 / 남은 금액
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

budget_card, budget_value = create_card(dashboard_frame, "💰 총 예산", f"{budget:,}원", "#1F497D")
used_card, used_value = create_card(dashboard_frame, "💸 현재 지출", "0원", "#1E40AF")
remain_card, remain_value = create_card(dashboard_frame, "💵 남은 금액", f"{budget:,}원", "#0F766E")

budget_card.grid(row=0, column=0, padx=(0, 5), sticky="ew") # sticky="w" : 왼쪽(west)에 붙임 / "e": 오른쪽(east)에 붙임 / "n": 위쪽(north)에 붙임 / "s": 아래쪽(sount)에 붙임 ex) "ex": 왼쪽과 오른쪽에 모두 붙어라
used_card.grid(row=0, column=1, padx=5, sticky="ew")
remain_card.grid(row=0, column=2, padx=(5, 0), sticky="ew")

# anchor : 위젯 내부(or 배정된 공간)에서 내용(텍스트 등)을 어디에 붙일지 결정
# sticky : grid 셀 안의 위젯에서 위젯을 어디에 붙이고 얼마나 늘릴지 결정
# => anchor은 내용의 정렬, sticky는 위젯의 배치와 확장 개념

# 예산 사용률 프로그래스 바 및 상태 표시
progress = ttk.Progressbar(
    dashboard_frame,
    orient="horizontal", # horizontal: 가로
    mode="determinate", # determinate: 진행률이 있는 바(몇 %인지 표시). indeterminate: 왔다 갔다 하는 로딩바
    style="Green.Horizontal.TProgressbar"
)
progress.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
style.configure("Green.Horizontal.TProgressbar", troughcolor="#E5E7EB", background="#22C55E") # troughcolor: 안채워진 부분 색 / background: 채워진 부분 색
style.configure("Orange.Horizontal.TProgressbar", troughcolor="#E5E7EB", background="#EA580C")
style.configure("Red.Horizontal.TProgressbar", troughcolor="#E5E7EB", background="#E11D48")

progress_status = tk.Label(dashboard_frame, text="예산 사용률 0%", font=("맑은 고딕", 10), bg="#F4F6F9", fg="#64748B")
progress_status.grid(row=2, column=0, columnspan=3, pady=(5, 10))


# ==========================================
# 6. 검색 및 필터 영역 (Search & Actions)
# ==========================================
list_frame = tk.Frame(window, bg="#F4F6F9")
list_frame.pack(fill="both", expand=True, padx=30, pady=10) # expand는 부모 창에 남는 공간을 위젯이 가져갈지 결정. true면 남는 공간이 있을 경우 이 위젯에게 배분함

# 검색 바 (Search Bar)
search_frame = tk.Frame(list_frame, bg="#F4F6F9")
search_frame.pack(fill="x", pady=(0, 12))

# ------------------------------------------
# [좌측] 검색어 입력, 필터, 초기화
# ------------------------------------------
left_search_frame = tk.Frame(search_frame, bg="#F4F6F9")
left_search_frame.pack(side="left")

# 검색 창 및 필터링 스타일
entry_style = {
    "relief": "flat", # relief: 위젯의 테두리 모양 옵션. "solid": 실선, "flat": 테두리 없음 ...
    "bd": 0,
    "bg": "#FFFFFF",
    "fg": "#1E293B",
    "highlightbackground": "#CBD5E1",  # 비활성 시 테두리 색상
    "highlightcolor": "#1F497D",  # 포커스(클릭) 시 테두리 색상
    "highlightthickness": 1,  # 테두리 두께
}
style.configure(
    "TCombobox",
    fieldbackground="#FFFFFF",  # 기본 입력창 배경 (흰색)
    background="#F1F5F9", # 오른쪽 화살표 버튼 배경색
    bordercolor="#CBD5E1", # 테두리 색상
    arrowcolor="#475569", # 화살표 아이콘 색상
    padding=4,
) # style.configure(): 평상시 기본 모양
style.map(
    "TCombobox",
    fieldbackground=[("readonly", "#FFFFFF"), ("focus", "#FFFFFF")],
    selectbackground=[("readonly", "#FFFFFF"), ("focus", "#FFFFFF")],
    selectforeground=[("readonly", "#1E293B"), ("focus", "#1E293B")],
    bordercolor=[("focus", "#1F497D")],
) # style.map(): 위젯의 상태별 변화

# 1. 검색 결과 건수
search_count_label = tk.Label(
    left_search_frame,
    text="총 0건",
    font=("맑은 고딕", 9, "bold"),
    bg="#F4F6F9",
    fg="#64748B",
    width=8,
    anchor="w" # 상자 안에서 텍스트 왼쪽 정렬
)
search_count_label.pack(side="left", padx=(0, 8))

# 2. 검색 입력창 (Placeholder 적용)
search_entry = tk.Entry(left_search_frame, font=("맑은 고딕", 9), width=16, **entry_style)
search_entry.pack(side="left", padx=(0, 8), ipady=3)

# Placeholder 기능 (검색어 입력 힌트)
def on_search_focus_in(e):
    if search_entry.get() == "🔍 검색어 입력...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="#1E293B") # fg: 글자(텍스트) 색상

def on_search_focus_out(e):
    if not search_entry.get().strip():
        search_entry.insert(0, "🔍 검색어 입력...")
        search_entry.config(fg="#94A3B8")

search_entry.insert(0, "🔍 검색어 입력...")
search_entry.config(fg="#94A3B8")
search_entry.bind("<FocusIn>", on_search_focus_in)
search_entry.bind("<FocusOut>", on_search_focus_out)
search_entry.bind("<KeyRelease>", lambda e: search_money())

# 3. 분류 필터
tk.Label(left_search_frame, text="분류", font=("맑은 고딕", 9), bg="#F4F6F9", fg="#475569").pack(side="left", padx=(4, 4))
category_filter = ttk.Combobox(
    left_search_frame,
    values=["전체", "예식장", "스드메", "스냅영상", "맞춤정장", "예물", "신혼여행", "가전", "가구", "생활용품", "기타"],
    width=8,
    state="readonly"
)
category_filter.current(0)
category_filter.pack(side="left", padx=(0, 8))
category_filter.bind("<<ComboboxSelected>>", lambda e: search_money())

# 4. 결제수단 필터
tk.Label(left_search_frame, text="결제수단", font=("맑은 고딕", 9), bg="#F4F6F9", fg="#475569").pack(side="left", padx=(0, 4))
payment_filter = ttk.Combobox(
    left_search_frame,
    values=["전체", "신용카드", "체크카드", "현금", "계좌이체"],
    width=8,
    state="readonly"
)
payment_filter.current(0)
payment_filter.pack(side="left", padx=(0, 8))
payment_filter.bind("<<ComboboxSelected>>", lambda e: search_money())

# "<KeyRelease>" → 일반 이벤트 (기본 이벤트)
# "<<ComboboxSelected>>" → 가상 이벤트 (Virtual Event)

# 5. 초기화 버튼
reset_button = tk.Button(
    search_frame,
    text="↻",
    command=lambda: reset_search(),
    font=("맑은 고딕", 9, "bold"),
    bg="#94A3B8",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=8,
    pady=3
)
reset_button.pack(side="left")

# ------------------------------------------
# [우측] 관리 버튼들 (추가 / 수정 / 삭제)
# ------------------------------------------
right_action_frame = tk.Frame(search_frame, bg="#F4F6F9")
right_action_frame.pack(side="right")

# 우측 관리 버튼들 (추가 / 수정 / 삭제)
del_btn = tk.Button(
    right_action_frame,
    text="🗑 삭제",
    command=lambda: delete_money(),
    font=("맑은 고딕", 9, "bold"),
    bg="#EF4444",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=10,
    pady=3,
)
del_btn.pack(side="right", padx=(4, 0))

edit_btn = tk.Button(
    right_action_frame,
    text="✏ 수정",
    command=lambda: open_edit_dialog(),
    font=("맑은 고딕", 9, "bold"),
    bg="#64748B",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=10,
    pady=3,
)
edit_btn.pack(side="right", padx=(4, 0))

add_btn = tk.Button(
    right_action_frame,
    text="➕ 추가",
    command=lambda: open_add_dialog(),
    font=("맑은 고딕", 9, "bold"),
    bg="#1F497D",
    fg="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=10,
    pady=3,
)
add_btn.pack(side="right", padx=(4, 0))


# ==========================================
# 7. 내역 목록 (Treeview)
# ==========================================
# 표(Treeview) 디자인 세부 설정
# 데이터 영역(행/셀)
style.configure("Treeview", font=("맑은 고딕", 10), rowheight=30, background="white", fieldbackground="white", borderwidth=0) # background: 전체 배경 색 / fieldbackground: 각 셀의 배경색
# 헤더 영역
style.configure("Treeview.Heading", font=("맑은 고딕", 10, "bold"), background="#E2E8F0", foreground="#333333", relief="flat")
# 상태(선택됨, 눌림 등)에 따른 변화
style.map("Treeview", background=[("selected", "#E0F2FE")], foreground=[("selected", "#0369A1")])

tree_container = tk.Frame(list_frame, bg="white", highlightbackground="#E2E8F0", highlightthickness=1)
tree_container.pack(fill="both", expand=True)

money_list = ttk.Treeview(tree_container, columns=("date", "category", "item", "shop", "price", "payment"), show="headings", height=8) # show="headings": 트리 표시(#0 컬럼)는 숨기고, 컬럼 제목(heading)만 보여줘라. 기본값은 tree
scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=money_list.yview) # money_list.yview: Treeview → Scrollbar. 스크롤바 움직이면 Treeview의 세로 위치를 바꿔라
money_list.configure(yscrollcommand=scrollbar.set) # scrollbar.set: Scrollbar → Treeview. Treeview가 현재 위치를 스크롤바에 알려줘라

money_list.heading("date", text="날짜", command=lambda: sort_column("date"))
money_list.heading("category", text="분류", command=lambda: sort_column("category"))
money_list.heading("item", text="항목", command=lambda: sort_column("item"))
money_list.heading("shop", text="구매처", command=lambda: sort_column("shop"))
money_list.heading("price", text="금액", command=lambda: sort_column("price"))
money_list.heading("payment", text="결제수단", command=lambda: sort_column("payment"))

money_list.column("date", width=90, anchor="center")
money_list.column("category", width=70, anchor="center")
money_list.column("item", width=160, anchor="w", stretch=True) # stretch=True: 가용 공간을 채움
money_list.column("shop", width=130, anchor="center")
money_list.column("price", width=100, anchor="e")
money_list.column("payment", width=90, anchor="center")

money_list.bind("<Double-1>", lambda e: open_edit_dialog()) # 더블클릭 연동

money_list.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Treeview 생성 직후 안내 라벨 하나 생성
no_data_label = tk.Label(
    tree_container,
    text="등록된 지출 내역이 없습니다.",
    font=("맑은 고딕", 11),
    bg="white",
    fg="#94A3B8",
)

# ==========================================
# 8. 하단 요약 및 통계 그래프 영역 (Footer)
# ==========================================
footer_frame = tk.Frame(window, bg="#F4F6F9")
footer_frame.pack(fill="x", padx=30, pady=(5, 20))

# ------------------------------------------
# [하단 좌측] 총 지출 표시 & 백업/복원 버튼
# ------------------------------------------
db_btn_frame = tk.Frame(footer_frame, bg="#F4F6F9")
db_btn_frame.pack(side="left")

backup_button = tk.Button(
    db_btn_frame, text="💾 백업", command=backup_database,
    font=("맑은 고딕", 9, "bold"), bg="#E2E8F0", fg="#475569", 
    relief="flat", bd=0, cursor="hand2", padx=8, pady=3 
)
backup_button.pack(side="left", padx=2)

restore_button  = tk.Button(
    db_btn_frame, text="🔄 복원", command=lambda: restore_database(window),
    font=("맑은 고딕", 9, "bold"), bg="#E2E8F0", fg="#475569", 
    relief="flat", bd=0, cursor="hand2", padx=8, pady=3
)
restore_button .pack(side="left", padx=2)

total_label = tk.Label(db_btn_frame, text="총 지출 : 0원", font=("맑은 고딕", 11, "bold"), bg="#F4F6F9", fg="#1E293B")
# total_label.pack(side="left", padx=(0, 15))

# ------------------------------------------
# [하단 우측] 통계 & 내보내기 버튼 (주요 기능)
# ------------------------------------------
stat_btn_frame = tk.Frame(footer_frame, bg="#F4F6F9")
stat_btn_frame.pack(side="right")

stats_btn = tk.Button(
    stat_btn_frame, text="📈 통계", command=open_statistics,
    font=("맑은 고딕", 9, "bold"), bg="#475569", fg="white", activeforeground="white",
    activebackground="#334155", relief="flat", bd=0, cursor="hand2", padx=10, pady=4
)
stats_btn.pack(side="left", padx=3)

excel_button = tk.Button(
    stat_btn_frame, text="📄 Excel 저장", command=excel_export, # command=excel_export: lambda를 쓸 필요가 없는 이유는 매개변수를 전달하지 않는 함수이기 때문
    font=("맑은 고딕", 9, "bold"), bg="#0D9488", fg="white", 
    relief="flat", bd=0, cursor="hand2", padx=10, pady=4 
)
excel_button.pack(side="left", padx=3)

csv_button = tk.Button(
    stat_btn_frame, text="📄 CSV 저장", command=csv_export_file, # command=csv_export: lambda를 쓸 필요가 없는 이유는 매개변수를 전달하지 않는 함수이기 때문
    font=("맑은 고딕", 9, "bold"), bg="#4D7C0F", fg="white", 
    relief="flat", bd=0, cursor="hand2", padx=10, pady=4 
)
csv_button.pack(side="left", padx=3)

# side: 위젯을 어느 방향으로 배치할지 (side는 pack()에서만 사용하는 옵션)
# anchor: 배치된 공간 안에서 위젯(또는 내용)을 어느 쪽에 붙일지

# command=func 가장 기본. 버튼을 누르면 test() 실행
# command=func() 사용하면 안됨. 프로그램 실행하자마자 함수가 실행
# command=lambda: func() 함수에 인자를 넣고 싶을 때 사용. lambda는 이걸 나중에 실행하라는 예약표 개념
# bind(..., lambda e: func()) 이벤트용. 

# ==========================================
# 9. SQLlite 설정
# ==========================================
database.create_database()

# ==========================================
# 10. 프로그램 시작 실행
# ==========================================
load_data()
display_data()
update_total()
refresh_budget_entry()

window.mainloop() # 이벤트 루프 시작(창이 종료될 때까지 프로그램 실행)