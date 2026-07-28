import os

from openpyxl import Workbook
from openpyxl.styles import Font

# 상태(State)를 가지고 있으면 Class & 기능만 수행하면 Function. 즉, 기능이 많아지고 상태를 관리해야 하면 Class.
def export_excel(money_data):
    # 엑셀파일
        workbook = Workbook() # workbook(): 엑셀 파일 자체를 만드는 객체
    
        # 엑셀 안의 첫 번째 시트
        worksheet = workbook.active # active: 현재 선택되어 있는 시트 가져오기
    
        # 시트 이름 변경
        worksheet.title = "WeddingMoney"
    
        # 헤더
        worksheet.append([
            "날짜",
            "분류",
            "항목",
            "구매처",
            "금액",
            "결제수단"
        ])
    
        # 데이터
        for money in money_data:
            worksheet.append([
                money["date"],
                money["category"],
                money["item"],
                money.get("shop", ""),
                money["price"],
                money.get("payment", "")
            ])
    
        # Excel 저장
        workbook.save("WeddingMoney.xlsx")
    
        # Excel 자동 실행
        os.startfile("WeddingMoney.xlsx")