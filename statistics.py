import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt # 그래프를 만들기 위한 matplotlib 라이브러리 불러오기 (pyplot: 그래프 그리는 기능)
import matplotlib.font_manager as fm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.money_data = money_data

        self.create_widgets()

    # 클래스 안의 함수는 첫번째 인자로 무조건 self가 필요함!!
    def create_widgets(self):
        title = tk.Label(
            self,
            text="신혼 자금 통계",
            font=("맑은 고딕", 16, "bold")
        )

        title.pack(pady=20)

        # 통계 요약 카드
        self.create_summary_cards()

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        category_btn = tk.Button(
            btn_frame,
            text="지출 비교",
            command=self.show_category_bar_chart
        )

        category_btn.pack(
            side="left",
            padx=10
        )

        ratio_btn = tk.Button(
            btn_frame,
            text="카테고리 비율",
            command=self.show_category_pie_chart
        )

        ratio_btn.pack(
            side="left",
            padx=10
        )

        monthly_btn = tk.Button(
            btn_frame,
            text="월별 지출 추이",
            command=self.show_monthly_line_chart
        )

        monthly_btn.pack(
            side="left",
            padx=10
        )

        payment_btn = tk.Button(
            btn_frame,
            text="결제수단 분석",
            command=self.show_payment_bar_chart
        )

        payment_btn.pack(
            side="left",
            padx=10
        )

        top5_btn = tk.Button(
            btn_frame,
            text="지출 TOP 5",
            command=self.show_top5_expense
        )

        top5_btn.pack(
            side="left",
            padx=10
        )

    # ----------------------------------------------------
    # 통계 요약 카드 생성
    # ----------------------------------------------------
    def create_summary_cards(self):
        card_frame = tk.Frame(self)
        card_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        total_price = sum(
            money["price"]
            for money in self.money_data
        )

        category_total = self.calculate_category_total()

        if category_total:
            max_category = max(
                category_total,
                key=category_total.get
            )
        else:
            max_category = "-"

        count = len(self.money_data)

        cards = [
            ("총 지출", f"{total_price:,}원"),
            ("최대 지출", max_category),
            ("등록 건수", f"{count}건"),
        ]

        for title, value in cards:
            card = tk.Frame(
                card_frame,
                bg="#FFFFFF",
                bd=1,
                relief="solid",
                width=200,
                height=80
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            title_label = tk.Label(
                card,
                text=title,
                font=("맑은 고딕", 10, "bold"),
                bg="#FFFFFF",
                fg="#64748B"
            )

            title_label.pack(
                pady=(10, 2)
            )

            value_label = tk.Label(
                card,
                text=value,
                font=("맑은 고딕", 14, "bold"),
                bg="#FFFFFF",
                fg="#1E293B"
            )

            value_label.pack()

    # ----------------------------------------------------
    # 그래프 표사
    # ----------------------------------------------------
    # Matplotlib로 만든 그래프(fig)를 Tkinter 창 안의 특정 영역(chart_frame)에 표시하는 함수
    def display_chart(self, fig): # fig: matplotlib에서 만든 그래프 전체
        # 기존 그래프 제거
        for widget in self.chart_frame.winfo_children(): # winfo_children(): 현재 Frame 안에 들어있는 위젯 목록을 가져와
            widget.destroy() # destroy(): 위젯 제거

        canvas = FigureCanvasTkAgg( # Matplotlib → Tkinter 연결. 즉, matplotlib Figure -> FigureCanvasTkAgg -> Tkinter Widget 이 구조
            fig, # 넣을 그래프
            master=self.chart_frame # 어디에 넣을지 지정
        )

        canvas.draw() # 그래프 그리기

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
    
        plt.title(
            "카테고리별 지출 현황",
            fontsize=13,
            fontweight="bold",
            pad=15,
            color="#0F172A",
        )
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
    
        plt.title(
            "신혼 자금 사용 비율",
            fontsize=13,
            fontweight="bold",
            pad=15,
            color="#0F172A",
        )
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
        ax.plot(
            months,
            prices,
            marker="o", # o: ● / s: ■ / ^: ▲ / x: ✕
            linewidth=2
        ) # ax.plot(x축데이터, y축데이터): 선 그래프를 그리는 함수

        # 점 위 금액 표시
        for x, y in zip(months, prices):
            ax.text(
                x,
                y,
                f"{y/10000:,.0f}만원", # ,: 천단위 쉼표 / .0f: 소수점 없이 출력
                ha="center", # Horizontal Alignment(가로정렬)
                va="bottom", # Vertical Alignment(세로정렬)
                fontsize=9
            ) # ax.text(x좌표, y좌표, 출력할문자)

        ax.set_title(
            "월별 지출 추이",
            fontsize=13,
            fontweight="bold",
            pad=15
        )

        ax.spines["top"].set_visible(False) # spine: 그래프를 둘러싸고 있는 테두리 선
        ax.spines["right"].set_visible(False)

        ax.grid(axis="y", alpha=0.3) # grid(): 격자선(Grid) 그리는 함수 / axis="y": y축 방향으로만 격자선 그리기 / alpha: 투명도

        plt.xticks(rotation=45) # x축 글자 45도 회전
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

        fig, ax = plt.subplots(
            figsize=(8,5),
            facecolor="#F8FAFC"
        )
        ax.set_facecolor("#F8FAFC")

        bars = ax.barh(
            payments, # y축
            prices, # x축(막대길이)
            color="#10B981",
            height=0.55
        ) # 막대 그래프 생성. bar: 세로 / barh: 가로
        # ax.bar(x, 막대높이 height)
        # ax.barh(y, 막대길이 width)

        if bars:
            bars[-1].set_color("#059669") # 파이썬에서 -1은 마지막 요소를 의미함. 즉, 막대그래프의 마지막 막대 객체를 의미

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
        # ax.spines["left"].set_color("#CBD5E1")
    
        ax.xaxis.set_visible(False)  # X축 수치 눈금 제거
    
        plt.title(
            "결제수단별 지출 현황",
            fontsize=13,
            fontweight="bold",
            pad=15,
            color="#0F172A",
        )
        plt.tight_layout() # 여백 자동 맞춤

        self.display_chart(fig)

    # ----------------------------------------------------
    # 지출 TOP5
    # ----------------------------------------------------
    def show_top5_expense(self):
        if not self.money_data:
            messagebox.showinfo("통계", "등록된 지출 내역이 없습니다.")
            return

        sorted_data = sorted(
            self.money_data,
            key=lambda x: x["price"],
            reverse=True
        ) # sorted(정렬할 데이터, key=정렬 기준, reverse=정렬 방향)

        top5 = sorted_data[:5]

        fig, ax = plt.subplots(
            figsize=(8,5),
            facecolor="#F8FAFC"
        )

        ax.set_axis_off() # ax.set_axis_off()는 그래프의 축(axis)을 전부 숨기는 함수. 즉, 이 Axes(그래프 영역)의 축, 눈금, 테두리, 라벨을 모두 끄겠다는 뜻
        ax.text(
            0.02,
            0.95,
            "🏆 지출 TOP 5",
            fontsize=14,
            fontweight="bold",
            color="#0F172A"
        )

        y = 0.83 # 텍스트를 표시할 처음 y 위치
        # ax.text(x좌표, y좌표, 내용)인데 앞에서 ax.set_axis_off() 이걸 했기 때문에 y위치를 지정하는 것. 보통 좌표는 0~1 범위로 사용(높은곳은 1, 낮은곳은 0)
        for idx, money in enumerate(top5, start=1): # enumerate(): 순서 번호와 값을 같이 가져오는 함수
            text = (
                f"{idx}. {money['item']}\n"
                f"   {money['date']} · {money['category']}\n"
                f"   {money['price']:,}원"
            )

            ax.text(
                0.03,
                y,
                text,
                fontsize=10.5,
                va="top",
                color="#334155"
            )

            y -= 0.18

        plt.tight_layout()
        self.display_chart(fig)