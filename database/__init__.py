# __init__.py는 이 폴더를 파이썬 패키지로 만들어주는 파일
# __init__.py 파일이 있으면, datebase라는 폴더를 패키지로 인식
# Python 3.3 이후부터는 __init__.py 없어도 동작 가능

from .init_db import create_database

from .expense import (
    add_expense,
    get_all_expenses,
    get_expenses,
    update_expense,
    delete_expense
)

from .settings import (
    get_setting,
    update_setting
)

from .category import (
    get_category_list,
    get_all_categories,
    add_category,
    update_category,
    is_category_used,
    delete_category
)

# database 패키지에서 자주 사용하는 기능을 외부에 노출
# 그래서 main.py에서는:
#
# 기존:
# from database.expense import get_all_expenses
#
# 변경:
# from database import get_all_expenses
#
# 처럼 간단하게 사용할 수 있음
# 즉, database라는 큰 모듈 하나처럼 사용 가능