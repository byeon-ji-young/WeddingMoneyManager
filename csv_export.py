import csv
from tkinter import filedialog
from tkinter import messagebox

import database

def csv_export_file():
    expenses = database.get_all_expenses()

    if not expenses:
        messagebox.showinfo("알림", "내보낼 데이터가 없습니다.")
        return

    file_path = filedialog.asksaveasfilename( # filedialog.asksaveasfilename: 사용자가 어디에 저장할지 선택하는 창을 띄우기
        defaultextension=".csv", # 기본 확장자
        filetypes=[("CSV 파일", "*.csv")] # 파일 선택창에서 CSV 파일만 보임
    )

    if not file_path: # 취소 버튼을 클릭하면 file_path가 "" 라서 함수 종료
        return

    # CSV 파일 열기
    with open(
        file_path,
        "w", # write 모드. 파일 없으면 생성, 있으면 기존 내용 삭제 후 새로 작성
        encoding="utf-8-sig", # utf-8 사용 시 한글 CSV를 엑셀에서 열 때 한글이 깨질 수 있어서 utf-8-sig 사용
        newline="" # CSV 파일 작성 시 줄바꿈 문제를 방지
    ) as file:

        # CSV 작성 객체 생성
        writer = csv.writer(file) # CSV 파일에 데이터를 쓰는 도구 만들기

        # 제목 행 작성
        writer.writerow([
            "날짜",
            "카테고리",
            "항목",
            "구매처",
            "금액",
            "결제수단"
        ])

        # 실제 데이터 작성
        for expense in expenses:
            writer.writerow([
                expense["date"],
                expense["category"],
                expense["item"],
                expense["shop"],
                expense["price"],
                expense["payment"]
            ])

    messagebox.showinfo("완료", "CSV 파일 저장 완료")