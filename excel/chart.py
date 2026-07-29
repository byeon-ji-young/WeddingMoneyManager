from openpyxl.chart import BarChart, Reference #BarChart: 막대 차트 객체, Reference: 어느 셀을 차트 데이터로 사용할지 지정 

def create_category_chart(worksheet, category_data):
    """
    카테고리별 지출 막대 차트 생성
    """

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    chart_row = 2
    
    for category, price in category_data:
        worksheet[f"H{chart_row}"] = category
        worksheet[f"I{chart_row}"] = price

        chart_row += 1

    worksheet.column_dimensions["H"].hidden = True
    worksheet.column_dimensions["I"].hidden = True

    CATEGORY_COL = 8 # H열
    PRICE_COL = 9 # I열

    # ----------------------------------------------------
    # 차트 생성
    # ----------------------------------------------------
    chart = BarChart() # 막대그래프 객체 생성

    # 데이터 범위 지정 - 세로축(Y축) 데이터
    data = Reference(worksheet, min_col=PRICE_COL, min_row=2, max_row=chart_row - 1) # Reference: 차트가 사용할 셀 범위 / min_col=9: 9번째 열(I열)

    # 카테고리 범위 지정 - 가로축(X축)
    categories = Reference(worksheet, min_col=CATEGORY_COL, min_row=2, max_row=chart_row - 1)

    # 차트에 연결 (데이터 추가, 카테고리 추가)
    chart.add_data(data)
    chart.set_categories(categories)

    # ----------------------------------------------------
    # 차트 설정
    # ----------------------------------------------------
    chart.visible_cells_only = False # 숨김 데이터도 읽기
    # chart.title = "카테고리별 지출"
    chart.type = "col" # bar: 가로 막대 그래프, col: 세로 막대 그래프
    chart.width = 14
    chart.height = 7
    # chart.legend = None
    chart.style = 10 # Excel 기본 스타일 번호

    # 시트에 추가
    worksheet.add_chart(chart, "A18") # A18: 왼쪽 위 시작 위치. 즉, A18부터 그래프가 그려짐

def create_payment_chart(worksheet, payment_data):
    """
    결제수단별 지출 막대 차트 생성
    """

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    chart_row = 2

    for payment, price in payment_data.items():
        worksheet[f"K{chart_row}"] = payment
        worksheet[f"L{chart_row}"] = price

        chart_row += 1

    worksheet.column_dimensions["K"].hidden = True
    worksheet.column_dimensions["L"].hidden = True

    PAYMENT_COL = 11 # K열
    PRICE_COL = 12   # L열

    # ----------------------------------------------------
    # 차트 생성
    # ----------------------------------------------------
    chart = BarChart()

    data = Reference(worksheet, min_col=PRICE_COL, min_row=2, max_row=chart_row - 1) 
    payments = Reference(worksheet, min_col=PAYMENT_COL, min_row=2, max_row=chart_row - 1)

    chart.add_data(data)
    chart.set_categories(payments)

    # ----------------------------------------------------
    # 차트 설정
    # ----------------------------------------------------
    chart.visible_cells_only = False
    chart.width = 14
    chart.height = 7
    chart.style = 10

    # 차트 위치
    worksheet.add_chart(chart, "J18")

def create_monthly_chart(worksheet, monthly_data):
    """
    월별 지출 추이 차트 생성
    """

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    chart_row = 2

    for month, price in sorted(monthly_data.items()):
        worksheet[f"N{chart_row}"] = month
        worksheet[f"O{chart_row}"] = price

        chart_row += 1

    MONTH_COL = 14 # N열
    PRICE_COL = 15 # O열

    # ----------------------------------------------------
    # 차트 생성
    # ----------------------------------------------------
    chart = BarChart()

    data = Reference(worksheet, min_col=PRICE_COL, min_row=2, max_row=chart_row - 1)
    months = Reference(worksheet, min_col=MONTH_COL, min_row=2, max_row=chart_row - 1)

    chart.add_data(data)
    chart.set_categories(months)

    # ----------------------------------------------------
    # 차트 설정
    # ----------------------------------------------------
    chart.width = 14
    chart.height = 7
    chart.style = 10
    chart.title = "월별 지출 추이"

    worksheet.add_chart(chart, "A35")