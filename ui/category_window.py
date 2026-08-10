import tkinter as tk # tk: 기본 Tkinter 위젯
from tkinter import ttk, messagebox # ttk: Tkinter의 개선된 UI 위젯

from database import (
    get_all_categories,
    add_category,
    update_category,
    is_category_used,
    delete_category
)

class CategoryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.title("카테고리 관리")
        self.geometry("380x500")
        self.resizable(False, False)
        self.configure(bg="#f8f9fa")  # 깔끔한 연회색 배경

        self.selected_category_id = None
        self.setup_styles()
        self.create_widgets()
        self.load_categories()

    # ttk 커스텀 스타일 설정
    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # 플랫폼 공통의 깔끔한 기본 테마

        # 프레임 배경
        self.style.configure("TFrame", background="#f8f9fa")
        
        # 라벨 스타일
        self.style.configure("Header.TLabel", font=("맑은 고딕", 12, "bold"), background="#f8f9fa", foreground="#1F497D")
        self.style.configure("TLabel", font=("맑은 고딕", 9), background="#f8f9fa", foreground="#495057")

        # Treeview 스타일
        self.style.configure(
            "Category.Treeview", # 스타일 이름(style name) 지정
            font=("맑은 고딕", 10),
            background="#f8f9fa",
            foreground="#333333",
            rowheight=28,
            fieldbackground="#f8f9fa",
            borderwidth=1,
            relief="solid"
        )

        # 선택했을 때 강조 색상 설정
        self.style.map(
            "Category.Treeview",
            background=[("selected", "#e7f5ff")],
            foreground=[("selected", "#1971c2")]
        )

        # 버튼 기본 스타일
        self.style.configure(
            "TButton",
            font=("맑은 고딕", 9, "bold"),
            padding=(10, 6),
            background="#e9ecef",
            # foreground="#212529",
            cursor="hand2",
            borderwidth=0,
        )
        self.style.map("TButton", background=[("active", "#dee2e6")])

        # 추가 버튼
        self.style.configure("Primary.TButton", background="#1F497D", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#1B3E68")])

        # 수정 버튼
        self.style.configure("Success.TButton", background="#E2E8F0", foreground="#1e293b")
        self.style.map("Success.TButton", background=[("active", "#CBD5E1")])

        # 삭제 버튼
        self.style.configure("Danger.TButton", background="#E2E8F0", foreground="#1e293b")
        self.style.map("Danger.TButton", background=[("active", "#CBD5E1")])

    def create_widgets(self):
        # 1. 헤더 영역
        header_frame = ttk.Frame(self, padding=(20, 15, 20, 10))
        header_frame.pack(fill="x")
        
        ttk.Label(header_frame, text="📁 카테고리 목록", style="Header.TLabel").pack(anchor="w")

        # 2. Treeview (리스트) & 스크롤바 영역
        list_frame = ttk.Frame(self, padding=(20, 0, 20, 10))
        list_frame.pack(fill="both", expand=True)
        
        # Treeview 생성 (헤더 표시 안함)
        self.tree = ttk.Treeview(
            list_frame,
            style="Category.Treeview",
            selectmode="browse",
            show="tree" # 표 헤더를 숨기고 목록 형태로만 사용
        )
        self.tree.column("#0", stretch=True)

        # 스크롤바 → Treeview
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview) # orient="vertical": 세로 스크롤바 (horizontal: 가로 스크롤바) / yview: Tkinter 위젯의 세로 스크롤 위치를 변경하는 함수 / self.tree.yview: Treeview를 위아래로 움직이는 함수

        # Treeview → 스크롤바
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y") # fill="y": 세로 채우기

        self.tree.bind("<<TreeviewSelect>>", self.on_select) # bind(): 이벤트와 함수를 연결하는 기능. 즉, 리스트박스에서 항목을 선택했을 때 실행할 함수 연결

        # <<TreeviewSelect>>: Tkinter의 가상 이벤트
        # on_select 함수에서 event를 받는 이유: bind()가 자동으로 이벤트 정보를 넘겨주기 때문

        # 실제 GUI동작 이벤트: 실제 사용자가 직접 하는 행동
        # "<Button-1>": 마우스 클릭
        # "<Dobule-Button-1>": 마우스 더블 클릭
        # "<key>": 키보드 입력
        # 
        # 가상이벤트(<< >>): Tkinter가 특정 상황을 묶어서 만들어 둔 이벤트
        # "<<ListboxSelect>>": 리스트 선택 변경
        # "<<ComboboxSelected>>": 콤보박스 선택 변경
        # "<<MyEvent>>" 내가 직접 만들 수도 있음 (event_generate("<<MyEvent>>")로 직접 만든 이벤트를 발생시켜야함!)
        # "<<TreeviewSelect>>": 행 선택 변경. listbox의 ListboxSelect와 동일한 기능

        # 3. 입력/수정 폼 영역 (팝업창 대신 화면 하단에 배치)
        form_frame = ttk.Frame(self, padding=(20, 10, 20, 10))
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="카테고리명 입력/수정").pack(anchor="w", pady=(0, 5))

        self.entry_name = ttk.Entry(form_frame, font=("맑은 고딕", 10))
        self.entry_name.pack(fill="x", ipady=6)

        # 4. 하단 버튼 영역
        button_frame = ttk.Frame(self, padding=(20, 10, 20, 20))
        button_frame.pack(fill="x")

        self.btn_add = ttk.Button(button_frame, text="추가", style="Primary.TButton", command=self.add_category)
        self.btn_add.pack(side="left", expand=True, fill="x", padx=(0, 4))

        self.btn_update = ttk.Button(button_frame, text="수정", style="Success.TButton", command=self.update_category)
        self.btn_update.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_delete = ttk.Button(button_frame, text="삭제", style="Danger.TButton", command=self.delete_category)
        self.btn_delete.pack(side="left", expand=True, fill="x", padx=(4, 0))

    # 카테고리 읽기
    def load_categories(self):
        # Listbox - 기존 목록 초기화
        # self.listbox.delete(0, tk.END)

        # Treeview - 기존 목록 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.categories = get_all_categories()

        for category in self.categories:
            # Listbox - 새로운 항목(문자열)을 추가
            # self.listbox.insert(tk.END, f"  {category['name']}") # listbox.insert(위치, 추가할_내용)

            # Treeview - 새로운 항목 추가(카테고리 ID를 iid로 매핑)
            self.tree.insert("", "end", iid=str(category["id"]), text=f"  {category['name']}")
            
        self.clear_form()

    # 폼 초기화
    def clear_form(self):
        self.selected_category_id = None
        self.entry_name.delete(0, tk.END)

    # 리스트 선택 시 입력창에 자동으로 띄워주기
    def on_select(self, event):
        # Listbox - 행 선택
        # selected = self.listbox.curselection() # curselection(): 현재 선택 상태를 가져오는 함수 / 즉, Listbox에서 현재 선택된 항목의 위치(인덱스) 가져오기
        # 
        # if not selected:
        #     return
        #  
        # index = selected[0] # Listbox 선택 결과는 튜플 형태로 반환됨 ex.(2,)
        #
        # category = self.categories[index]
        # self.selected_category_id = category["id"]
        #
        # self.entry_name.delete(0, tk.END)
        # self.entry_name.insert(0, category["name"])

        # Treeview - 행 선택
        selected_items = self.tree.selection()

        if not selected_items:
            return

        cat_id = selected_items[0]
        self.selected_category_id = int(cat_id)

        item_text = self.tree.item(cat_id, "text").strip() # item(): Treeview의 특정 행 정보를 가져오는 함수. 즉, text 속성을 가져오라는 뜻 / strip(): 문자열의 앞뒤 공백을 제거

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, item_text)

    # 카테고리 추가
    def add_category(self):
        name = self.entry_name.get().strip()

        if not name:
            messagebox.showwarning("입력 필요", "카테고리 이름을 입력해주세요.", parent=self) # parent=self: 이 메시지 창의 부모 창을 현재 창(self)으로 지정!
            return

        try:
            result = add_category(name)

            if result is None:
                messagebox.showwarning("중복", "이미 존재하는 카테고리입니다.", parent=self)
                return
            
            self.load_categories()
            
        except Exception as e:
            messagebox.showerror("오류", f"카테고리 추가 실패\n{e}", parent=self)

    # 카테고리 수정
    def update_category(self):
        if not self.selected_category_id:
            messagebox.showwarning("선택 필요", "수정할 카테고리를 목록에서 선택하세요.", parent=self)
            return

        name = self.entry_name.get().strip()

        if not name:
            messagebox.showwarning("입력 필요", "변경할 카테고리 이름을 입력하세요.", parent=self)
            return

        try:
            update_category(self.selected_category_id, name)

            self.load_categories()
        except Exception as e:
            messagebox.showerror("오류", f"카테고리 수정 실패\n{e}", parent=self)

    # 카테고리 삭제
    def delete_category(self):
        if not self.selected_category_id:
            messagebox.showwarning("선택 필요", "삭제할 카테고리를 목록에서 선택하세요.", parent=self)
            return

        name = self.entry_name.get().strip()

        result = messagebox.askyesno("삭제 확인", f"'{name}' 카테고리를 삭제하시겠습니까?", parent=self)

        if result:
            try:
                if is_category_used(name):
                    messagebox.showwarning("삭제 불가", "사용 중인 카테고리입니다.\n지출 내역을 먼저 변경해주세요.", parent=self)
                    return
                
                delete_category(self.selected_category_id)

                self.load_categories()
            except Exception as e:
                messagebox.showerror("오류", f"카테고리 삭제 실패\n{e}", parent=self)