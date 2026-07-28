# 분석(요약) 화면

import excel.styles as styles

from collections import defaultdict # defaultdict: 카테고리별 합계를 만들 때 사용

def create_summary_sheet(worksheet, money_data, budget):
    # 시트 이름
    worksheet.title = "대시보드"

    # ----------------------------------------------------
    # 데이터 계산
    # ----------------------------------------------------
    # 요약 데이터
    total_price = sum(money["price"] for money in money_data)

    # 예산 사용률
    usage_rate = 0
    if budget > 0:
        usage_rate = total_price / budget * 100

    # 카테고리별 지출
    category_data = defaultdict(int) # defaultdict(int): 처음 보는 키는 자동으로 만들어줌. 기본값이 0인 딕셔너리(dictionary)를 만드는 코드. 즉, category_data["가전"] = 0을 자동으로 만들어줌
    for money in money_data:
        category_data[money["category"]] += money["price"]

    # 금액 높은 순 정렬
    category_data = sorted(
        category_data.items(), # items(): {category: price, category2: price2, ...} 이 형태를 [(category, price), (category2, price2), ...] 형태로 바꿔줌
        key=lambda x: x[1], # lambda: 일회성 작은 함수를 만드는 문법 / x[1]: 두 번째 값(price)을 기준으로 정렬
        reverse=True # reverse=True: 내림차순
    )

    # 최근 지출 TOP 5
    top_expenses = sorted(
        money_data,
        key=lambda x: x["price"],
        reverse=True
    )[:5] # 리스트[시작:끝]: 끝 인덱스는 포함하지 않음. 즉, [:5]는 0번째부터 5번째 전까지 가져와라

    # 결제수단별 지출
    payment_data = defaultdict(int)
    for money in money_data:
        payment = money.get("payment", "미입력") # money["payment"]: payment가 없으면 keyError 발생. get("payment", "미입력"): 있으면 가져오고 아니면 미입력
        payment_data[payment] += money["price"]

    # ----------------------------------------------------
    # 1. 메인 제목 영역
    # ----------------------------------------------------
    worksheet.merge_cells("A1:F1")

    title_cell = worksheet["A1"] # worksheet["A1"]: A1 셀 하나 가져오기 / worksheet[1]: 1행(row)의 모든 셀 가져오기 / worksheet["A"]: A열(column)의 모든 셀 가져오기
    title_cell.value = "결혼 준비 대시보드"
    title_cell.font = styles.font_title
    title_cell.alignment = styles.align_center

    # 병합된 A1:F1 전체에 배경색 채우기
    for col in range(1, 7): # range(시작, 끝)은 끝은 포함하지 않음. 즉, 1 ~ 6을 의미함
        worksheet.cell(row=1, column=col).fill = styles.title_fill # worksheet.cell(): 원하는 셀 객체를 가져오기 / fill: 셀의 Fill(배경색)을 지정하는 속성

    # ----------------------------------------------------
    # 2. 예산 사용률
    # ----------------------------------------------------
    worksheet.merge_cells("A3:C3")
    worksheet["A3"] = "예산 사용률"

    worksheet.merge_cells("A4:C4")
    worksheet["A4"] = f"{usage_rate:.1f}%"

    worksheet.merge_cells("A5:C5")
    worksheet["A5"] = (
        f"{total_price:,}원 / {budget:,}원"
    )

    # ----------------------------------------------------
    # 3. 카테고리별 지출
    # ----------------------------------------------------
    worksheet.merge_cells("D3:F3")
    worksheet["D3"] = "카테고리별 지출"

    row = 4

    for category, price in category_data[:5]:
        worksheet.cell(
            row=row,
            column=4,
            value=category
        )

        worksheet.cell(
            row=row,
            column=6,
            value=price
        ).number_format = '#,##0"원"'

        row += 1

    # ----------------------------------------------------
    # 4. 최근 지출 TOP 5
    # ----------------------------------------------------
    worksheet.merge_cells("A8:B8")
    worksheet["A8"] = "최근 지출 TOP 5"

    worksheet["A9"] = "항목"
    worksheet["B9"] = "금액"

    row = 10

    for money in top_expenses:
        worksheet.cell(
            row=row,
            column=1,
            value=money["item"]
        )

        worksheet.cell(
            row=row,
            column=2,
            value=money["price"]
        ).number_format = '#,##0"원"'

        row += 1
    
    # ----------------------------------------------------
    # 5. 결제수단 분석
    # ----------------------------------------------------
    worksheet.merge_cells("D8:F8")
    worksheet["D8"] = "결제수단 분석"

    row = 9

    for payment, price in payment_data.items():
        worksheet.cell(
            row=row,
            column=4,
            value=payment
        )

        worksheet.cell(
            row=row,
            column=6,
            value=price
        ).number_format = '#,##0"원"'

        row += 1

    # ----------------------------------------------------
    # 기본 스타일
    # ----------------------------------------------------
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.alignment = styles.align_center
                cell.border = styles.border_all

    # ----------------------------------------------------
    # 열 너비
    # ----------------------------------------------------
    worksheet.column_dimensions["A"].width = 18
    worksheet.column_dimensions["B"].width = 18
    worksheet.column_dimensions["C"].width = 18
    worksheet.column_dimensions["D"].width = 18
    worksheet.column_dimensions["E"].width = 5
    worksheet.column_dimensions["F"].width = 18