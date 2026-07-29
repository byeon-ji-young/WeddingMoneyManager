from openpyxl.chart import BarChart, Reference, LineChart #BarChart: 막대 차트 객체, Reference: 어느 셀을 차트 데이터로 사용할지 지정
from openpyxl.chart.label import DataLabelList

# 차트 스타일 적용
def apply_chart_style(chart, title, width, style=10, show_labels=True):
    # ----------------------------------------------------
    # 차트 설정
    # ----------------------------------------------------
    chart.visible_cells_only = False # 숨김 데이터도 읽기
    chart.title = title
    chart.width = width
    chart.height = 7.5
    chart.legend = None
    chart.style = style # Excel 기본 스타일 번호
    # 축 제목
    # chart.x_axis.title = "카테고리"
    # chart.y_axis.title = "금액(만원)"
    # 축 표시 설정
    chart.x_axis.delete = False
    # chart.y_axis.delete = False
    # chart.y_axis.numFmt = '#,##0,"만원"' # 차트는 만원단위로 표시하려고 // 10000 추가했으니까 이 소스는 불필요함
    chart.y_axis.numFmt = '#,##0'
    # 눈금선 제거
    chart.y_axis.majorGridlines = None
    # Y축 최소값 0 지정
    chart.y_axis.scaling.min = 0

    # ----------------------------------------------------
    # 차트 라벨 설정
    # ----------------------------------------------------
    chart.dataLabels = DataLabelList()

    # 값만 표시
    chart.dataLabels.showVal = show_labels

    # 불필요한 항목 숨김
    chart.dataLabels.showCatName = False
    chart.dataLabels.showSerName = False
    chart.dataLabels.showLegendKey = False

    # chart.dataLabels.numFmt = '#,##0' 

# 차트 색상 설정
def set_series_color(chart, hex_color="1F497D"):
    """차트 시리즈(막대/선)의 색상을 상단 헤더(다크블루) 계열 단색으로 설정"""

    for series in chart.series:
        # 막대 그래프 채우기 색상 지정
        series.graphicalProperties.solidFill = hex_color
        # 꺾은선 그래프 선 색상 및 두께 지정
        series.graphicalProperties.line.solidFill = hex_color
        series.graphicalProperties.line.width = 25000  # 선 두께

def create_category_chart(worksheet, category_data):
    """카테고리별 지출 막대 차트 생성"""

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    worksheet["H1"] = "카테고리"
    worksheet["I1"] = "금액(만원)"

    chart_row = 2
    
    for category, price in category_data:
        worksheet[f"H{chart_row}"] = category
        worksheet[f"I{chart_row}"] = price // 10000 # //: 정수 나눗셈(Floor Division). 소수점 버리고 몫만 남김
        worksheet[f"I{chart_row}"].number_format = '#,##0'

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

    # 차트에 연결 - 데이터 추가, 카테고리 추가
    # chart.add_data(data, titles_from_data=True) # titles_from_data=True: 첫 번째 행을 데이터 제목(Series 이름) 으로 사용할지 결정
    chart.add_data(data)
    chart.set_categories(categories)

    apply_chart_style(chart, "카테고리별 지출 (만원)", 22.5, style=2)
    # chart.type = "col" # bar: 가로 막대 그래프, col: 세로 막대 그래프
    chart.gapWidth = 50

    set_series_color(chart, "1F497D")

    # ----------------------------------------------------
    # 시트에 추가
    # ----------------------------------------------------
    worksheet.add_chart(chart, "A18") # A18: 왼쪽 위 시작 위치. 즉, A18부터 그래프가 그려짐

def create_payment_chart(worksheet, payment_data):
    """결제수단별 지출 막대 차트 생성"""

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    worksheet["K1"] = "결제수단"
    worksheet["L1"] = "금액(만원)"
    
    chart_row = 2

    for payment, price in payment_data.items():
        worksheet[f"K{chart_row}"] = payment
        worksheet[f"L{chart_row}"] = price // 10000
        worksheet[f"L{chart_row}"].number_format = '#,##0'

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

    apply_chart_style(chart, "결제수단별 지출 (만원)", 7.5, style=2)
    chart.gapWidth = 50

    set_series_color(chart, "1F497D")

    # ----------------------------------------------------
    # 시트에 추가
    # ----------------------------------------------------
    worksheet.add_chart(chart, "A32")

def create_monthly_chart(worksheet, monthly_data):
    """월별 지출 추이 차트 생성"""

    # ----------------------------------------------------
    # 차트 데이터 생성
    # ----------------------------------------------------
    worksheet["N1"] = "년월"
    worksheet["O1"] = "금액(만원)"

    chart_row = 2

    for month, price in sorted(monthly_data.items()):
        worksheet[f"N{chart_row}"] = month
        worksheet[f"O{chart_row}"] = price // 10000
        worksheet[f"O{chart_row}"].number_format = '#,##0'

        chart_row += 1

    MONTH_COL = 14 # N열
    PRICE_COL = 15 # O열

    worksheet.column_dimensions["N"].hidden = True
    worksheet.column_dimensions["O"].hidden = True

    # ----------------------------------------------------
    # 차트 생성
    # ----------------------------------------------------
    chart = LineChart()

    data = Reference(worksheet, min_col=PRICE_COL, min_row=2, max_row=chart_row - 1)
    months = Reference(worksheet, min_col=MONTH_COL, min_row=2, max_row=chart_row - 1)

    chart.add_data(data)
    chart.set_categories(months)

    apply_chart_style(chart, "월별 지출 추이 (만원)", 15, style=2)
    chart.dLbls.dLblPos = "t" # dLblPos: 라벨 위치 지정(t:top, b:bottom, l:left, r:right, ctr:center)
    chart.varyColors = False # varyColors: 각 가로값(데이터 포인트)마다 색 바뀌는 옵션
    # 직선 연결 (과도한 곡선 왜곡 방지)
    chart.smooth = False

    # 라인차트 마커
    line_series = chart.series[0] # series[0]: 첫 번째 데이터 계열(Series). chart.add_data(data)를 호출하면 Series가 1개 생성 - 금액(원). 만약에 뒤에 열을 추가하면 series[0]은 금액, series[1]은 추가열
    line_series.marker.symbol = "circle"
    line_series.marker.size = 7
    line_series.marker.graphicalProperties.solidFill = "1F497D"
    line_series.marker.graphicalProperties.line.noFill = True # noFill: 테두리 없애기

    set_series_color(chart, "1F497D")

    # ----------------------------------------------------
    # 시트에 추가
    # ----------------------------------------------------
    worksheet.add_chart(chart, "C32")