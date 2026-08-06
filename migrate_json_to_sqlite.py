import json
import database

def migrate():
    # ==========================================
    # JSON 데이터 읽기
    # ==========================================
    with open("money_backup.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # 기존 데이터 가져오기
    money_data = data.get("money_data", [])

    # 지출 내역 저장
    count = 0

    # ==========================================
    # expenses 테이블 저장
    # ==========================================
    for money in money_data:
        expense = {
            "date": money["date"],
            "category": money["category"],
            "item": money["item"],
            "shop": money.get("shop", ""),
            "price": money["price"],
            "payment": money.get("payment", "")
        }

        database.add_expense(expense)

        count += 1

    # ==========================================
    # settings 테이블 budget 저장
    # ==========================================
    budget = data.get("budget", 0)

    database.update_setting("budget", str(budget))

    print(f"변환 완료 : {count}개 데이터 이동")

# ==========================================
# 직접 실행할 때만 실행
# ==========================================
if __name__ == "__main__":
    database.create_database()

    migrate()