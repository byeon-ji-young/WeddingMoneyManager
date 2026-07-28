import os

from openpyxl import Workbook
from datetime import datetime

from excel.detail import create_detail_sheet

today = datetime.now().strftime("%Y-%m-%d")

# 상태(State)를 가지고 있으면 Class & 기능만 수행하면 Function. 즉, 기능이 많아지고 상태를 관리해야 하면 Class.
def export_excel_file(money_data, budget):
    # 엑셀파일
    workbook = Workbook() # workbook(): 엑셀 파일 자체를 만드는 객체

    # 엑셀 안의 첫 번째 시트
    worksheet = workbook.active # active: 현재 선택되어 있는 시트 가져오기

    # 시트 이름
    worksheet.title = "WeddingMoney"

    # 눈금선 보이게 설정
    worksheet.views.sheetView[0].showGridLines = True

    create_detail_sheet(worksheet, money_data, budget)

    # 저장
    filename = f"결혼준비비용_{today}.xlsx"
    workbook.save(filename)

    # 자동 실행
    os.startfile(filename)