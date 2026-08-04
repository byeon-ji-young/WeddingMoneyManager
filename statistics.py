import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt # 그래프를 만들기 위한 matplotlib 라이브러리 불러오기 (pyplot: 그래프 그리는 기능)
import matplotlib.font_manager as fm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Matplotlib으로 그린 그래프(Figure)를 Tkinter 창(GUI) 안에 붙여넣을 수 있는 위젯(종이)으로 변환해 주는 다리(연결고리) 역할

# Matplotlib 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic" # or plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# StatisticsWindow는 tk.Toplevel을 기반으로 만든 새로운 클래스
class StatisticsWindow(tk.Toplevel): # 괄호 안은 상속(inheritance)을 의미. tk.Toplevel은 새로운 별도 창. 즉, Tkinter의 새 창 기능을 물려받아서 새로운 창을 만드는 클래스
    # 파이썬 규칙상, 클래스 안에서 만드는 함수(메서드)는 첫 번째 인자로 무조건 self를 받도록 약속되어 있음!
    def __init__(self, parent, money_data): # __init__: 팝업창 초기화 (모달 설정, 창 크기/위치 지정) / self: 이 클래스로 만든 객체 자기 자신
        super().__init__(parent) # 부모 창(main.py의 window) 위에 뜨는 자식 창(Toplevel)으로 지정

        self.title("통계 분석")
        self.geometry("800x600")
        self.configure(bg="#F8FAFC")

        self.money_data = money_data
        self.current_key = "category_bar"

        self.create_widgets()

    # 클래스 안의 함수는 첫번째 인자로 무조건 self가 필요함!!
    def create_widgets(self):
        title = tk.Label(
            self,
            text="결혼 비용 통계",
            font=("맑은 고딕", 13, "bold"),
            bg="#F8FAFC",
            fg="#0F172A"
        )
        title.pack(side="top", pady=(15, 10))

        # 통계 요약 카드
        self.create_summary_cards()

        # 버튼 프레임
        self.btn_frame = tk.Frame(self, bg="#F8FAFC")
        self.btn_frame.pack(side="top", fill="x", padx=20, pady=(10, 10))

        self.chart_frame = tk.Frame(self, bg="#F8FAFC")
        self.chart_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 15))

        # 버튼 생성 및 딕셔너리에 저장
        self.buttons = {}
        btn_list = [
            ("category_bar", "지출 비교", self.show_category_bar_chart),
            ("category_pie", "지출 비율", self.show_category_pie_chart),
            ("monthly_line", "월별 지출 추이", self.show_monthly_line_chart),
            ("payment_bar", "결제수단 분석", self.show_payment_bar_chart),
            ("top5", "지출 TOP 5", self.show_top5_expense),
        ]

        for key, text, command in btn_list:
            btn = tk.Button(
                self.btn_frame,
                text=text,
                command=lambda k=key, cmd=command: self.select_tab(k, cmd), # 'lambda k=key, cmd=command:' 이 형태로 현재값 고정. 이것을 lambda 기본값 캡쳐라고 함
                font=("맑은 고딕", 9),
                bg="#FFFFFF",
                fg="#475569",
                activebackground="#F1F5F9",
                activeforeground="#0F172A",
                bd=0,
                relief="flat",
                highlightbackground="#CBD5E1",
                highlightthickness=1,
                cursor="hand2",
                padx=14,
                pady=5
            )
            btn.pack(side="left", padx=4)

            # 호버 효과
            # btn.bind("<Enter>", lambda e, b=btn, k=key: self.on_btn_hover(b, k, True))
            # btn.bind("<Leave>", lambda e, b=btn, k=key: self.on_btn_hover(b, k, False))

            self.buttons[key] = btn # 생성한 버튼을 딕셔너리에 저장

        # 기본 첫 화면으로 지출 비교 차트 표시
        self.select_tab("category_bar", self.show_category_bar_chart)

    # 마우스 호버
    def on_btn_hover(self, btn, key, is_hover):
        # 현재 선택되어 있는 탭이 아닐 때만 호버 효과 적용
        if getattr(self, "current_key", "") != key: # getattr(객체, "속성이름", 기본값). 즉, self 안에 current_key가 있으면 가져오고, 없으면 빈 문자열("")을 반환하라는 뜻
            if is_hover:
                btn.config(bg="#F1F5F9", fg="#0F172A", highlightbackground="#94A3B8")
            else:
                btn.config(bg="#FFFFFF", fg="#475569", highlightbackground="#CBD5E1")
                
    # 선택된 버튼의 디자인을 바꿔주는 함수
    def select_tab(self, selected_key, command):
        self.current_key = selected_key

        for key, btn in self.buttons.items():
            if key == selected_key:
                # 선택된 버튼: 파란색 배경 + 흰색 글씨 + 강조 효과
                btn.config(
                    bg="#1E293B",
                    fg="#FFFFFF",
                    font=("맑은 고딕", 9, "bold"),
                    highlightbackground="#1E293B",
                )
            else:
                # 선택 안 된 버튼: 흰색 배경 + 연한 회색 글씨
                btn.config(
                    bg="#FFFFFF",
                    fg="#475569",
                    font=("맑은 고딕", 9),
                    highlightbackground="#CBD5E1",
                )
        
        command() # 해당 그래프 실행
    
    # ----------------------------------------------------
    # 통계 요약 카드 생성 (총 지출 / 주요 결제수단 / 최대 지출 / 등록 건수)
    # ----------------------------------------------------
    def create_summary_cards(self):
        card_frame = tk.Frame(self, bg="#F8FAFC")
        card_frame.pack(side="top", fill="x", padx=15, pady=(0, 5))

        total_price = sum(money["price"] for money in self.money_data)
        count = len(self.money_data)

        # 1. 주요 결제수단 및 비율 계산
        payment_total = {}
        for money in self.money_data:
            pay_method = money.get("payment", money.get("pay_method", "기타")) # 딕셔너리.get(키, 기본값). payment 확인 -> 있으면 반환 없으면 기본값 실행 -> pay_method 확인 -> 있으면 반환 없으면 기타 반환
            
            payment_total[pay_method] = (
                payment_total.get(pay_method, 0) + money["price"]
            )

        if payment_total and total_price > 0:
            top_pay = max(payment_total, key=payment_total.get) # key=payment_total.get: 비교할 때는 키 자체가 아니라, 그 키의 값을 기준으로 비교해라
            top_pay_pct = (payment_total[top_pay] / total_price) * 100
            pay_text = f"{top_pay} ({top_pay_pct:.1f}%)"
        else:
            pay_text = "-"

        # 2. 카테고리별 최대 지출 분야 및 금액 계산
        category_total = self.calculate_category_total()
        if category_total:
            max_cat = max(category_total, key=category_total.get) # key=category_total.get: 비교할 때는 키 자체가 아니라, 그 키의 값을 기준으로 비교해라
            max_val = category_total[max_cat]
            if max_val >= 10000:
                max_text = f"{max_cat} ({max_val/10000:,.0f}만원)"
            else:
                max_text = f"{max_cat} ({max_val:,}원)"
        else:
            max_text = "-"

        
        # 카드 데이터 구성 (타이틀, 값, 포인트 컬러)
        cards_data = [
            ("총 지출", f"{total_price:,}원", "#2563EB"),
            ("주요 결제수단", pay_text, "#10B981"),
            ("최대 지출", max_text, "#8B5CF6"),
            ("등록 건수", f"{count}건", "#F59E0B"),
        ]

        for title, value, color in cards_data:
            card = tk.Frame(
                card_frame,
                bg="#FFFFFF",
                bd=1,
                relief="flat",
                highlightbackground="#E2E8F0",
                highlightthickness=1,
            )
            card.pack(side="left", expand=True, fill="x", padx=4)

            # 상단 컬러 포인트 바
            top_bar = tk.Frame(card, bg=color, height=3)
            top_bar.pack(fill="x", side="top")

            # card.pack_propagate(False) # Tkinter에서 부모 위젯(Frame 등)의 크기가 자식 위젯 때문에 자동으로 바뀌는 것을 막는 코드. 즉, 이 카드(card)는 내가 정한 크기를 유지하고, 안에 들어가는 내용물 크기에 맞춰 자동으로 커지지 마라는 뜻

            title_label = tk.Label(
                card,
                text=title,
                font=("맑은 고딕", 8, "bold"),
                bg="#FFFFFF",
                fg="#64748B"
            )
            title_label.pack(pady=(7, 2))

            value_label = tk.Label(
                card,
                text=value,
                font=("맑은 고딕", 11, "bold"),
                bg="#FFFFFF",
                fg="#0F172A"
            ).pack(pady=(0, 7))

    # ----------------------------------------------------
    # 그래프 표시
    # ----------------------------------------------------
    # Matplotlib로 만든 그래프(fig)를 Tkinter 창 안의 특정 영역(chart_frame)에 표시하는 함수
    def display_chart(self, fig): # fig: matplotlib에서 만든 그래프 전체
        # 기존 그래프 제거
        for widget in self.chart_frame.winfo_children(): # winfo_children(): 현재 Frame 안에 들어있는 위젯 목록을 가져와
            widget.destroy() # destroy(): 위젯 제거

        # 1단계: Matplotlib로 만든 그래프(fig)와 넣을 Tkinter 영역(self.chart_frame)을 연결
        canvas = FigureCanvasTkAgg( # Matplotlib → Tkinter 연결. 즉, matplotlib Figure -> FigureCanvasTkAgg -> Tkinter Widget 이 구조
            fig, # 넣을 그래프
            master=self.chart_frame # 어디에 넣을지 지정
        )

        # 2단계: Canvas에 그래프를 실제로 렌더링(그리기)
        canvas.draw() # 그래프 그리기

        # 3단계: Tkinter가 인식할 수 있는 '위젯' 형태로 변환해서 화면에 배치 (.pack() 사용 가능!)
        canvas.get_tk_widget().pack( # et_tk_widget(): Tkinter 위젯으로 변환. 즉, FigureCanvasTkAgg -> Tkinter Widget로 변환해라
            fill="both", # both: 가로, 세로 모두 채움
            expand=True # 남는 공간을 가져감
        )

        plt.close(fig) # 메모리에서 그래프 제거
        # plt.close(): 현재 활성화된 그래프 닫기
        # plt.close(fig): 특정 그래프(fig)만 닫기 - 권장
        # plt.close("all"): 열려 있는 모든 그래프 닫기 

    # ----------------------------------------------------
    # 카테고리별 지출 금액 계산
    # ----------------------------------------------------
    def calculate_category_total(self):
        category_total = {}

        if not self.money_data:
            return {}

        for money in self.money_data:
            category = money["category"]
            price = money["price"]

            if category in category_total:
                category_total[category] += price
            else:
                category_total[category] = price

        return category_total

    # ----------------------------------------------------
    # Matplotlib - 카테고리별 지출 Bar Chart
    # ----------------------------------------------------
    def show_category_bar_chart(self):
        category_total = self.calculate_category_total()

        if not category_total:
            messagebox.showinfo("통계", "표시할 데이터가 없습니다.")
            return

        # # matplotlib은 리스트 형태를 선호함
        # categories = list(category_total.keys()) # keys(): 기능 실행, keys: 기능 자체. ex)get()
        # prices = list(category_total.values())
    
        # plt.figure(figsize=(8,5))
        # bars = plt.bar(categories, prices, color="#3B82F6") # 막대 그래프 생성. bar: 세로 / barh: 가로
        # for bar in bars:
        #     height = bar.get_height()
        #     plt.text(
        #         bar.get_x() + bar.get_width()/2,
        #         height,
        #         f"{height/10000:.0f}만원",
        #         ha="center",
        #         va="bottom"
        #     )

        # 금액이 작은 순서 -> 큰 순서로 정렬 (가로 막대 그래프는 아래에서 위로 그려짐)
        sorted_items = sorted(category_total.items(), key=lambda x: x[1]) # x[1]: 정렬 기준은 두 번째 값으로 하라는 뜻(x[0]: 가전, x[1]:1000)
        categories = [x[0] for x in sorted_items] # 카테고리만 뽑기
        prices = [x[1] for x in sorted_items] # 가격만 뽑기
    
        fig, ax = plt.subplots(figsize=(8, 5), facecolor="#F8FAFC") # fig(Figure): 전체 종이, ax(Axes): 실제 그래프가 그려지는 영역
        ax.set_facecolor("#F8FAFC") # 그래프가 그려지는 부분 배경
    
        # 가로 막대 그래프 생성 (barh)
        bars = ax.barh(categories, prices, color="#3B82F6", height=0.55, zorder=3)
    
        # 가장 큰 금액 강조 (맨 위 막대 색상 차별화)
        if bars:
            bars[-1].set_color("#1D4ED8") # 파이썬에서 -1은 마지막 요소를 의미함. 즉, 막대그래프의 마지막 막대 객체를 의미함
    
        # 막대 옆 금액 라벨 표시
        max_price = max(prices) if prices else 1
        for bar in bars:
            width = bar.get_width() # 막대의 길이. 즉, 값(price)을 의미
            if width > 0:
                val_text = (
                    f"{width/10000:,.0f}만원"
                    if width >= 10000
                    else f"{width:,.0f}원"
                )
                ax.text(
                    width + (max_price * 0.015),
                    bar.get_y() + bar.get_height() / 2,
                    f"{val_text}",
                    va="center",
                    ha="left",
                    fontsize=9.5,
                    fontweight="bold",
                    color="#1E293B",
                )
    
        # 불필요한 테두리 및 눈금선 정리 (1e7 표기 원천 제거)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E1")
    
        ax.xaxis.set_visible(False)  # X축 수치 눈금 제거
        # tick: 눈금 표시. tick_params(): 눈금 색상,크기,방향,길이,표시여부 등 조절하는 함수
        ax.tick_params(axis="y", colors="#334155", labelsize=10) # axis="y": y축 눈금만 변경 / colors: 눈금글자, 눈금선 다 적용
    
        # plt.title(
        #     "카테고리별 지출 현황",
        #     fontsize=13,
        #     fontweight="bold",
        #     pad=15,
        #     color="#0F172A",
        # )
        # plt.xlabel("카테고리")
        # plt.ylabel("금액")
        plt.tight_layout() # 여백 자동 맞춤
        # plt.show() # 새 창 띄워서 그래프 표시. 같은 창 안에서 그래프 변경하려고 이거 주석하고 self.display_chart(fig)로 변경함. 새 창 안뜸
        self.display_chart(fig)

    # ----------------------------------------------------
    # Matplotlib - 카테고리별 지출 비율 Pie Chart
    # ----------------------------------------------------
    def show_category_pie_chart(self):
        category_total = self.calculate_category_total()

        if not category_total:
            messagebox.showinfo("통계", "표시할 데이터가 없습니다.")
            return

        # categories = list(category_total.keys())
        # prices = list(category_total.values())
    
        # max_index = prices.index(max(prices))
        # explode = [0] * len(prices)
        # explode[max_index] = 0.1
    
        # plt.figure(figsize=(6,6))
        # wedges, texts, autotexts = plt.pie(
        #     prices,
        #     labels=None,
        #     autopct=make_autopct(prices),
        #     startangle=90, # 기본은 3시 방향부터 시작하는데 90도를 주면 12시 방향부터 시작함
        #     wedgeprops={"width": 0.45}, # 도넛형 그래프
        #     explode=explode, # 자동으로 살짝 튀어나오게
        #     textprops={"fontsize": 9}
        # ) # 원형 그래프 생성
    
        # 금액이 큰 순서대로 정렬
        sorted_items = sorted(category_total.items(), key=lambda x: x[1], reverse=True)
        categories = [x[0] for x in sorted_items]
        prices = [x[1] for x in sorted_items]
    
        colors = [
            "#2563EB",
            "#3B82F6",
            "#60A5FA",
            "#93C5FD",
            "#A855F7",
            "#EC4899",
            "#F43F5E",
            "#10B981",
            "#F59E0B",
            "#64748B",
        ]
    
        fig, ax = plt.subplots(figsize=(7.5, 5.5), facecolor="#F8FAFC")
    
        # 도넛 차트 생성
        wedges, texts, autotexts = ax.pie( # wedges: 각 조각(부채꼴) ex.wedges[0]: 첫번째 원 조각, texts: 라벨 텍스트, autotexts: 원 안에 표시되는 숫자 텍스트
            prices,
            labels=None,  # 원 조각 위 라벨 지우기 (우측 범례로 대체)
            autopct=self.make_autopct(prices),
            startangle=90, # 기본은 3시 방향부터 시작하는데 90도를 주면 12시 방향부터 시작함
            colors=colors[: len(prices)], # list[:]: 리스트 슬라이싱 형식(리스트[시작:끝])
            pctdistance=0.75,  # 퍼센트 위치 조정. 퍼센트 글자가 위치하는 거리
            wedgeprops={
                "width": 0.42,
                "edgecolor": "white",
                "linewidth": 2,
            },  # 도넛 모양과 테두리 설정
            textprops={"fontsize": 8.5, "weight": "bold"}, # 텍스트 스타일 설정
        )
    
        # 퍼센트 텍스트 색상 흰색으로 고정
        for autotext in autotexts:
            autotext.set_color("white")
    
        # 우측 범례(Legend) 설정 (카테고리명 + 금액 깔끔하게 표시)
        total_val = sum(prices)
        legend_labels = [
            f"{category} ({price/total_val*100:.1f}%)" for category, price in zip(categories, prices) # zip(): 두 리스트를 같은 위치끼리 묶는 역할
        ]
    
        plt.legend( # legend(): 범례 만드는 함수
            wedges, # 색상 표시 객체
            legend_labels, # 표시할 글자
            # title="카테고리",
            loc="center left", # 범례 기준 위치 정하기. 즉, center left는 범례 박스의 왼쪽 가운데를 기준점으로 삼겠다는 뜻
            # bbox_to_anchor=(1, 0, 0.5, 1), # 범례 위치를 세밀하게 조정. bbox_to_anchor=(x 위치, y 위치, width, height)
            bbox_to_anchor=(1, 0.5),
            frameon=False, # 범례 테두리 제거
            labelcolor="#334155"
        )
        # loc은 '범례 박스의 어느 점을 기준점으로 삼을지' 결정하고, bbox_to_anchor는 '그 기준점을 어디에 놓을지' 결정한다
        # (0,1)            (1,1)
        #   +----------------+
        #   |                |
        #   |                |
        #   |                |
        #   |                |
        #   +----------------+
        # (0,0)            (1,0)
        # 왼쪽 아래 = (0,0) / 오른쪽 아래 = (1,0) / 오른쪽 위 = (1,1). 즉, 나는 오른쪽 아래에 기준 영역을 만든다는 뜻
    
        # plt.title(
        #     "신혼 자금 사용 비율",
        #     fontsize=13,
        #     fontweight="bold",
        #     pad=15,
        #     color="#0F172A",
        # )
        plt.axis("equal") # 원형으로 맞춤
        plt.tight_layout()
        # plt.show() # 같은 창 안에서 그래프 변경하려고 이거 주석하고 self.display_chart(fig)로 변경함. 새 창 안뜸
        self.display_chart(fig)
    
    # 파이 차트 수치 라벨 가독성 처리
    def make_autopct(self, values): # 설정값(values)을 기억하는 함수를 만들어서 반환하는 역할 (함수를 만들어서 반환하는 함수: 클로저(closure))
        def my_autopct(percent): # percent는 matplotlib가 자동으로 넣어주는 값. matplotlib이 사용할 함수
            total = sum(values)
            price = int(total * percent / 100)
            
            if percent < 4:
                #return f"{percent:.1f}%"
                return ""
            else:
                # return f"{percent:.1f}%\n({price:,}원)"
                return f"{percent:.1f}%"
    
        return my_autopct

    # ----------------------------------------------------
    # 월별 지출 금액 계산
    # ----------------------------------------------------
    def calculate_monthly_total(self):
        monthly_total = {}

        if not self.money_data:
            return {}

        for money in self.money_data:
            date = money["date"]
            month = date[:7]  # 앞 7글자 자르기
            price = money["price"]

            if month in monthly_total:
                monthly_total[month] += price
            else:
                monthly_total[month] = price
                

        return monthly_total

    # ----------------------------------------------------
    # Matplotlib - 월별 지출 추이 Line Chart
    # ----------------------------------------------------
    def show_monthly_line_chart(self):
        monthly_total = self.calculate_monthly_total()

        if not monthly_total:
            messagebox.showinfo("통계", "표시할 데이터가 없습니다.")
            return

        # 날짜 순서 정렬
        # items()는 딕셔너리(dictionary)의 키(key)와 값(value)을 한 쌍으로 가져오는 메서드
        sorted_items = sorted(monthly_total.items()) # items(): {category: price, category2: price2, ...} 이 형태를 [(category, price), (category2, price2), ...] 형태로 바꿔줌

        months = [x[0] for x in sorted_items]
        prices = [x[1] for x in sorted_items]

        fig, ax = plt.subplots(figsize=(7,5), facecolor="#F8FAFC") # fig(Figure): 전체 종이, ax(Axes): 실제 그래프가 그려지는 영역
        ax.set_facecolor("#F8FAFC")

        ax.fill_between(months, prices, color="#3B82F6", alpha=0.12) # ax.fill_between(x축, y축): 선 그래프 아래쪽 영역을 색칠하는 함수 / alpha: 투명도

        # 메인 라인 및 포인트 마커 스타일
        ax.plot(
            months,
            prices,
            color="#2563EB",
            marker="o", # o: ● / s: ■ / ^: ▲ / x: ✕
            markersize=7,
            markerfacecolor="#FFFFFF", # 마커 안쪽 색상
            markeredgecolor="#2563EB",
            markeredgewidth=2,
            linewidth=2.5,
            zorder=3 # zorder: 겹치는 요소의 앞뒤 순서. 숫자가 클수록 위에 그려짐
        ) # ax.plot(x축데이터, y축데이터): 선 그래프를 그리는 함수

        # 점 위 금액 표시
        max_price = max(prices) if prices else 1
        for x, y in zip(months, prices):
            val_text = f"{y/10000:,.0f}만원" if y >= 10000 else f"{y:,.0f}원" # ,: 천단위 쉼표 / .0f: 소수점 없이 출력

            ax.text(
                x,
                y + (max_price * 0.05),
                val_text,
                ha="center", # Horizontal Alignment(가로정렬)
                va="bottom", # Vertical Alignment(세로정렬)
                fontsize=9,
                fontweight="bold",
                color="#334155",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.8) # bbox: 텍스트 주변에 박스(배경 상자)를 그리는 옵션
            ) # ax.text(x좌표, y좌표, 출력할문자)

        # ax.set_title(
        #     "월별 지출 추이",
        #     fontsize=13,
        #     fontweight="bold",
        #     pad=15
        # )

        # y축 범위에 여백 추가
        # ylim: y축의 최소값과 최대값 설정
        ax.set_ylim(0, max_price * 1.22) # y축(세로축)의 표시 범위를 직접 지정하는 코드. 즉, y축은 0부터 시작해서 최대값은 max_price의 122%까지만 표시하라는 뜻

        ax.spines["top"].set_visible(False) # spine: 그래프를 둘러싸고 있는 테두리 선
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#CBD5E1")

        # ax.yaxis.set_visible(False) # y축 수치 눈금 깔끔하게 숨김 (y축 전체 숨김)
        ax.tick_params(axis="y", labelleft=False, left=False) # labelleft: 왼쪽 숫자 라벨, left: 왼쪽 tick
        
        ax.tick_params(axis="x", colors="#475569", labelsize=9.5) # tick_params(): 축 눈금(tick)의 스타일을 변경
        
        ax.grid(axis="y", color="#E2E8F0", linestyle="--", alpha=0.3) # grid(): 격자선(Grid) 그리는 함수 / axis="y": y축 방향으로만 격자선 그리기 / alpha: 투명도

        plt.xticks(rotation=0) # x축 글자 회전 설정 (ex.rotation=45: 45도 회전, rotation=0: 회전 없음)
        plt.tight_layout() # tight_layout(): 그래프의 여백을 자동으로 조정하는 함수

        self.display_chart(fig)

    # ----------------------------------------------------
    # 결제수단별 지출 금액 계산
    # ----------------------------------------------------
    def calculate_payment_total(self):
        payment_total = {}

        if not self.money_data:
            return {}

        for money in self.money_data:
            payment = money["payment"]
            price = money["price"]

            if payment in payment_total:
                payment_total[payment] += price
            else:
                payment_total[payment] = price

        return payment_total

    # ----------------------------------------------------
    # Matplotlib - 결제수단별 지출 Bar Chart
    # ----------------------------------------------------
    def show_payment_bar_chart(self):
        payment_total = self.calculate_payment_total()

        if not payment_total:
            messagebox.showinfo("통계", "표시할 데이터가 없습니다.")
            return

        # 금액이 작은 순서 -> 큰 순서로 정렬 (가로 막대 그래프는 아래에서 위로 그려짐)
        sorted_items = sorted(
            payment_total.items(),
            key=lambda x: x[1]
        )

        payments = [x[0] for x in sorted_items]
        prices = [x[1] for x in sorted_items]

        # palette = ["#34D399", "#10B981", "#059669", "#047857"]
        # bar_colors = [palette[i % len(palette)] for i in range(len(payments))]

        fig, ax = plt.subplots(
            figsize=(8,5),
            facecolor="#F8FAFC"
        )
        ax.set_facecolor("#F8FAFC")

        bars = ax.barh(
            payments, # y축
            prices, # x축(막대길이)
            color="#3B82F6",
            height=0.5,
            zorder=3
        ) # 막대 그래프 생성. bar: 세로 / barh: 가로
        # ax.bar(x, 막대높이 height)
        # ax.barh(y, 막대길이 width)

        # 최대값 강조
        if bars:
            bars[-1].set_color("#1D4ED8") # 파이썬에서 -1은 마지막 요소를 의미함. 즉, 막대그래프의 마지막 막대 객체를 의미

        # 막대 옆 금액 라벨 표시
        total_pay = sum(prices)
        max_price = max(prices) if prices else 1
        for bar in bars:
            width = bar.get_width() # 막대의 길이. 즉, 값(price)을 의미
            if width > 0:
                percent = (width / total_pay) * 100
                val_text = (
                    f"{width/10000:,.0f}만원 ({percent:.1f}%)"
                    if width >= 10000
                    else f"{width:,.0f}원 ({percent:.1f}%)"
                )
                ax.text(
                    width + (max_price * 0.015),
                    bar.get_y() + bar.get_height() / 2, # 막대의 세로 가운데 위치. get_y(): 막대의 시작 위치 / get_height: 막대 높이
                    f"{val_text}",
                    va="center", # Vertical Alignment(세로정렬)
                    ha="left", # Horizontal Alignment(가로정렬)
                    fontsize=9.5,
                    fontweight="bold",
                    color="#1E293B",
                ) # ax.text(x좌표, y좌표, 출력할문자)
    
        # 불필요한 테두리 및 눈금선 정리 (1e7 표기 원천 제거)
        ax.spines["top"].set_visible(False) # spine: 그래프를 둘러싸고 있는 테두리 선
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E1")
    
        ax.xaxis.set_visible(False)  # x축 수치 눈금 제거
        ax.tick_params(axis="y", colors="#334155", labelsize=10)

        # plt.title(
        #     "결제수단별 지출 현황",
        #     fontsize=13,
        #     fontweight="bold",
        #     pad=15,
        #     color="#0F172A",
        # )
        plt.tight_layout() # 여백 자동 맞춤

        self.display_chart(fig)

    # ----------------------------------------------------
    # 지출 TOP5
    # ----------------------------------------------------
    def show_top5_expense(self):
        if not self.money_data:
            messagebox.showinfo("통계", "등록된 지출 내역이 없습니다.")
            return

        # 금액이 큰 순서대로 정렬
        sorted_data = sorted(
            self.money_data,
            key=lambda x: x["price"],
            reverse=True
        ) # sorted(정렬할 데이터, key=정렬 기준, reverse=정렬 방향)

        top5 = sorted_data[:5]

        fig, ax = plt.subplots(figsize=(8, 5), facecolor="#F8FAFC") # figsize=(가로, 세로) 인치 / facecolor: 배경색

        # 축 및 눈금선 숨기기 & 좌표계(0~1) 명시적 고정
        ax.set_axis_off() # ax.set_axis_off()는 그래프의 축(axis)을 전부 숨기는 함수. 즉, 이 Axes(그래프 영역)의 축, 눈금, 테두리, 라벨을 모두 끄겠다는 뜻
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # 제목 표시
        # ax.text(
        #     0.03,
        #     0.96,
        #     "🏆 지출 TOP 5",
        #     fontsize=13,
        #     fontweight="bold",
        #     color="#0F172A",
        #     va="top"
        # )

        # 등수별 색상 및 메달 설정
        rank_styles = [
            {"badge": "1위", "color": "#F59E0B"},
            {"badge": "2위", "color": "#64748B"},
            {"badge": "3위", "color": "#B45309"},
            {"badge": "4위", "color": "#94A3B8"},
            {"badge": "5위", "color": "#94A3B8"},
        ]

        y = 0.90 # 텍스트를 표시할 처음 y 위치 (0~1 기준)
        # ax.text(x좌표, y좌표, 내용)인데 앞에서 ax.set_axis_off() 이걸 했기 때문에 y위치를 지정하는 것. 보통 좌표는 0~1 범위로 사용(높은곳은 1, 낮은곳은 0)
        y_spacing = 0.18  # 항목 간 간격

        for idx, money in enumerate(top5, start=0): # enumerate(): 순서 번호와 값을 같이 가져오는 함수
            # 1. 순위 배지
            style = rank_styles[idx]

            ax.text(
                0.03,
                y,
                f"[{style['badge']}]",
                fontsize=10.5,
                fontweight="bold",
                color=style["color"],
                va="top", # Vertical Alignment(세로정렬)
            ) # ax.text(x좌표, y좌표, 표시할문자)

            # 2. 항목명 & 세부 정보 (날짜, 카테고리, 구매처)
            shop_text = f" ({money['shop']})" if money.get("shop") else ""
            item_text = f"{money['item']}{shop_text}"
            sub_text = f"{money['date']}  |  {money['category']}"

            ax.text(
                0.12,
                y,
                item_text,
                fontsize=10,
                fontweight="bold",
                color="#0F172A",
                va="top",
            )
            ax.text(
                0.12,
                y - 0.06,
                sub_text,
                fontsize=8,
                color="#64748B",
                va="top",
            )

            # 3. 금액
            price_text = f"{money['price']:,}원"

            ax.text(
                0.95,
                y - 0.01,
                price_text,
                fontsize=10.5,
                fontweight="bold",
                color="#1E293B",
                ha="right",
                va="top",
            )

            # 4. 카드 하단 구분선
            if idx < len(top5) - 1:
                ax.plot(
                    [0.03, 0.95],
                    [y - 0.13, y - 0.13],
                    color="#E2E8F0",
                    linewidth=1,
                    linestyle="-",
                ) # plot(): 선 그래프를 그리는 함수. ax.plot(x좌표 리스트, y좌표 리스트)

            y -= y_spacing  # 다음 항목 위치로 이동

        # tight_layout 대신 수동 패딩 지정 (텍스트 잘림 방지)
        fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.02)

        self.display_chart(fig)

# plt는 Matplotlib의 상태 기반(state-based) 방식. 즉, 현재 선택되어 있는 그래프에 작업하라는 뜻. 현재 활성화된 마지막 그래프에 적용
# plt.title(): 현재 활성화 된 그래프에 제목을 붙이는 방식 / ax.set_title(): 특정 Axes 객체에 직접 제목을 지정하는 방식
# 간단한 그래프 하나 → plt.title()도 괜찮음. 지금처럼 Tkinter + 여러 통계 화면 + 카드형 UI → ax.set_title() 사용 추천