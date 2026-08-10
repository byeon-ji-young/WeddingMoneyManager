# 📚 Python Desktop Application Development Log

> WeddingMoneyManager는 결혼 준비 비용 관리를 위해 제작한 Python 기반 Desktop Application이다.
> 초기 JSON 저장 방식에서 SQLite Database 구조로 개선하고, Tkinter GUI, Excel 자동화 Report, Windows 실행 파일 배포까지 전체 개발 과정을 기록한다.

---

# 1. Python 자료형(Data Type)

## List (리스트)

순서가 있는 여러 데이터를 저장하는 자료형

```python
numbers = [1, 2, 3]
```

### 자주 사용하는 메서드

| 함수 | 설명 |
|------|------|
| append() | 맨 뒤에 추가 |
| insert() | 원하는 위치에 추가 |
| remove() | 값으로 삭제 |
| pop() | 인덱스로 삭제 |
| clear() | 전체 삭제 |
| sort() | 정렬 |
| reverse() | 순서 뒤집기 |

예시

```python
money_data.append(dialog.result)
```

---

## Dictionary (딕셔너리)

Key : Value 형태의 자료구조 (Key와 Value를 한 쌍으로 저장하는 자료형)

```python
person = {
    "name":"홍길동",
    "age":30
}
```

### 자주 사용하는 메서드

| 함수 | 설명 |
|------|------|
| get() | Key가 없어도 오류 발생 안 함 |
| update() | 기존 데이터 수정 |
| keys() | Key 목록 |
| values() | Value 목록 |
| items() | Key와 Value 동시 반환 |
| pop() | Key 삭제 |
| clear() | 전체 삭제 |

예시

```python
money.get("payment", "")
```

```python
selected_data.update(dialog.result)
```

---

# 2. 반복문

## for

```python
for money in money_data:
```

---

## enumerate()

인덱스와 값을 동시에 가져온다.

```python
for index, money in enumerate(money_data):
```

---

## continue

현재 반복을 건너뛰고 다음 반복으로 이동

```python
if payment:
    continue
```

---

## break

반복 종료

```python
break
```

---

# 3. 조건문

```python
if

elif

else
```

예시

```python
if rate < 70:

elif rate < 100:

else:
```

---

# 4. 함수(Function)

함수 정의

```python
def hello():
```

호출

```python
hello()
```

---

## return

값 반환

```python
return total
```

---

## lambda

익명 함수(이름이 없는 함수)를 만드는 문법이다.

주로 Tkinter에서 버튼 클릭이나 이벤트 처리 시 함수의 실행을 나중으로 미루거나 인자를 전달할 때 사용한다.

```python
lambda x: x + 1
```

예시

```python
command=lambda: save_data("Wedding")
```

---

## command와 lambda

### command=func ⭐ 가장 많이 사용

버튼을 클릭했을 때 함수를 실행한다.

```python
command=save_data
```

버튼 클릭 시

```python
save_data()
```

가 실행된다.

> **괄호를 붙이지 않는다.**

---

### command=func() ❌ 사용하지 않음

```python
command=save_data()
```

프로그램이 실행되는 순간 함수가 바로 실행된다.

함수의 **실행 결과(None)** 가 `command`에 저장되므로 버튼을 눌러도 아무 동작을 하지 않는다.

---

### command=lambda: func(args)

함수에 **인자(Parameter)** 를 전달해야 할 때 사용한다.

```python
command=lambda: save_data("Wedding")
```

`lambda`는

> **"이 코드를 나중에 실행해."**

라는 의미의 익명 함수이다.

---

### bind(..., lambda e: func())

마우스 클릭, 더블클릭, 키 입력 등 **이벤트(Event)** 와 연결할 때 사용한다.

```python
money_list.bind("<Double-1>", lambda e: open_edit_dialog())
```

여기서 `e`는 **Event 객체**이다.

클릭 위치, 키 입력 등의 정보를 가지고 있으며, 필요하지 않으면 사용하지 않아도 된다.

---

### command와 bind 차이

| command | bind |
|----------|------|
| 버튼 클릭 전용 | 모든 이벤트 처리 |
| Event 객체 없음 | Event 객체(e) 전달 |
| 사용이 간단 | 다양한 이벤트 처리 가능 |

---

# 5. 클래스(Class)

클래스 정의

```python
class Person:
```

---

## __init__()

객체 생성 시 자동 실행

```python
def __init__(self):
```

---

## self

객체 자기 자신

```python
self.price_entry
```

---

## super()

부모 클래스 생성자 호출

```python
super().__init__(parent)
```

---

## 클래스(Class)와 함수(Function)의 차이

### 함수(Function)

하나의 기능만 수행할 때 사용한다.

예시

```python
def export_excel(money_data):
    ...
```

- 입력 데이터를 받아 처리
- 작업이 끝나면 종료
- 상태(State)를 유지하지 않음

---

### 클래스(Class)

관련된 데이터와 기능을 하나로 묶을 때 사용한다.

예시

```python
class ExpenseDialog:
```

클래스는 객체의 데이터와 메서드를 함께 관리한다.

```python
self.date_entry
self.category_combo
self.result
self.on_save()
```

### 언제 사용할까?

| 함수(Function) | 클래스(Class) |
|----------------|---------------|
| 기능 하나 수행 | 여러 기능과 데이터를 함께 관리 |
| 상태를 저장하지 않음 | 상태(State)를 유지 |
| export_excel() | ExpenseDialog |

---

# 6. 파일 입출력

## with open()

파일 열기

```python
with open("money.json")
```

---

## json.dump()

JSON 저장

```python
json.dump()
```

---

## json.load()

JSON 읽기

```python
json.load()
```

---

## try / except

예외 처리

```python
try:

except FileNotFoundError:
```

---

# 7. Tkinter

## Frame

영역을 나누는 컨테이너

```python
tk.Frame()
```

---

## Label

텍스트 표시

```python
tk.Label()
```

---

## Entry

텍스트 입력

```python
tk.Entry()
```

---

## Button

버튼

```python
tk.Button()
```

---

## Combobox

드롭다운 목록

```python
ttk.Combobox()
```

---

## Treeview

표 형태 데이터 표시

```python
ttk.Treeview()
```

---

## Scrollbar

스크롤바

```python
ttk.Scrollbar()
```

---

## Progressbar

진행률 표시

```python
ttk.Progressbar()
```

---

# 8. 레이아웃(Layout)

## pack()

자동 배치

```python
widget.pack()
```

자주 사용하는 옵션

- fill
- expand
- side
- anchor

---

## grid()

행/열 배치

```python
widget.grid()
```

자주 사용하는 옵션

- row
- column
- sticky
- padx
- pady

---

## columnconfigure()

열 비율 설정

```python
frame.columnconfigure(0, weight=1)
```

---

# 9. 이벤트(Event)

## bind()

이벤트 연결

```python
widget.bind()
```

### 자주 사용하는 이벤트

```python
<KeyRelease>
```

키 입력

```python
<Double-1>
```

더블 클릭

```python
<<ComboboxSelected>>
```

콤보박스 선택

---

## after()

일정 시간 후 함수 실행

```python
window.after(15, callback)
```

애니메이션 구현에 사용

---

# 10. Widget 제어

## config()

속성 변경

```python
label.config()
```

---

## get()

입력값 가져오기

```python
entry.get()
```

---

## set()

값 설정

```python
combobox.set()
```

---

## delete()

삭제

```python
entry.delete()
```

---

## insert()

삽입

```python
entry.insert()
```

---

# 11. Treeview

## insert()

Treeview에 새로운 행(Row)을 추가한다.

```python
tree.insert("", "end", values=(...))
```

---

## delete()

Treeview의 행을 삭제한다.

```python
tree.delete(item)
```

Treeview의 행을 전체 삭제한다.

```python
tree.delete(*tree.get_children())
```

---

## get_children()

Treeview의 모든 행 ID를 가져온다.

```python
tree.get_children()
```

---

## selection()

현재 선택된 행을 가져온다.

```python
tree.selection()
```

---

## selection_set()

특정 행을 선택 상태로 만든다.

```python
tree.selection_set(item)
```

---

## focus()

현재 포커스를 지정한다.

```python
tree.focus(item)
```

---

## see()

선택한 행이 보이도록 자동 스크롤한다.

```python
tree.see(item)
```

---

# 12. 자주 사용하는 내장 함수

```python
len()
```

길이

---

```python
sum()
```

합계

---

```python
min()
```

최솟값

---

```python
max()
```

최댓값

---

```python
abs()
```

절댓값

---

```python
int()
```

정수 변환

---

```python
str()
```

문자열 변환

---

```python
isinstance()
```

자료형 확인

---

# 13. Matplotlib

## figure()

그래프 생성

---

## bar()

막대 그래프

---

## pie()

원형 그래프

---

## text()

그래프 위에 텍스트 출력

---

## legend()

범례 표시

---

## tight_layout()

여백 자동 조정

---

## show()

그래프 출력

---

## Figure와 Axes 구조

Matplotlib은 Figure와 Axes 객체로 구성된다.

Figure:
- 전체 그래프 영역

Axes:
- 실제 그래프가 그려지는 영역


구조:

Figure
 └── Axes
      ├── Title
      ├── Axis
      └── Plot


Tkinter와 같이 여러 그래프를 관리하는 환경에서는 Axes 객체를 직접 제어하는 방식이 적합하다.

---

# 14. WeddingMoneyManager 주요 구현 함수

- display_data() → Treeview 데이터 화면 출력
- update_total() → 예산 및 지출 현황 계산
- search_money() → 검색 및 필터 기능 처리
- sort_column() → Treeview 컬럼 정렬
- animate_progress() → ProgressBar 애니메이션
- update_budget() → 예산 설정 변경
- export_excel() → Excel Report 생성
- database/ → SQLite 데이터 관리

※ 실제 구현 내용은 프로젝트 소스 코드(main.py 및 database/, ui/, utils/, excel/ 패키지 참고)

---

# 15. openpyxl (Excel 자동화)

WeddingMoneyManager의 Excel Report 생성 기능 구현을 위해 사용하였다.
주요 기능:
- 지출 상세 내역 시트 생성
- 예산 분석 Summary 시트 생성
- 셀 스타일 및 차트 적용

## Workbook

Excel 파일 자체를 의미한다.

```python
from openpyxl import Workbook

wb = Workbook()
```

---

## Worksheet

Excel 파일 내부의 하나의 시트를 의미한다.

```python
ws = wb.create_sheet("Summary")
```

---

## Cell
Excel의 개별 셀에 값을 입력한다.

```python
ws["A1"] = "총 예산"
```
 
---

## Cell Style

셀에 글꼴, 배경색, 테두리, 정렬 등의 디자인을 적용할 수 있다.

```python
cell.font = Font(...)
cell.fill = PatternFill(...)
cell.border = Border(...)
cell.alignment = Alignment(...)
```

---

## Chart

Excel 내부에 차트를 생성할 수 있다.

WeddingMoneyManager에서는
카테고리별 지출 분석과 월별 지출 추이 표시를 위해 사용하였다.

```python
from openpyxl.chart import BarChart, LineChart
from openpyxl.chart import Reference
```

---

# 16. ttk Style & UI 디자인

WeddingMoneyManager의 화면 개선 과정에서 기본 Tkinter 위젯만 사용하는 방식에서 벗어나 ttk.Style을 활용하여 UI 스타일을 관리하였다.

기존 문제:
- 위젯마다 개별 옵션 지정 필요
- 디자인 통일 어려움
- 코드 중복 증가

개선:
- ttk.Style 기반 공통 스타일 관리
- 입력 위젯 디자인 통일
- 버튼 및 Combobox 스타일 개선

---

## ttk.Style()

ttk 위젯의 기본 스타일을 변경한다.

```python
style = ttk.Style()

style.configure(
    "TButton",
    padding=5
)
```

---

## Theme 변경

Tkinter 기본 디자인 대신 ttk Theme을 적용할 수 있다.

```python
style.theme_use("clam")
```

사용 가능한 Theme:

- clam
- alt
- default
- classic

---

## LabelFrame

관련된 입력 요소를 그룹으로 묶는다.

```python
ttk.LabelFrame(
    parent,
    text="기본 정보"
)
```

WeddingMoneyManager에서는 입력 영역을 분리하기 위해 사용하였다.

구성:

### 기본 정보

- 날짜
- 카테고리
- 항목

### 결제 정보

- 구매처
- 금액
- 결제수단

---

# 17. Dashboard UI 설계

기존 Treeview 중심 화면에서 사용자가 중요한 정보를 빠르게 확인할 수 있도록 Dashboard 형태의 UI로 개선하였다.

주요 구성:

- 예산 Card
- 총 지출 Card
- 잔액 Card
- 예산 사용률 표시
- 지출 분석 Chart
- 최근 지출 TOP 5


## Card UI

Tkinter에는 기본 Card 위젯이 없기 때문에 Frame과 Label을 조합하여 직접 구현하였다.

구조:

```text
Frame
 ├── Label (제목)
 └── Label (값)
```

예시:

```python
card = tk.Frame(parent)

title = tk.Label(card)
value = tk.Label(card)
```

---

# 18. Matplotlib + Tkinter 연동

Matplotlib 그래프를 Tkinter 화면 내부에 표시하기 위해 FigureCanvasTkAgg를 사용하였다.

```python
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
```

사용 흐름:

## 1. Figure 생성

```python
fig = plt.figure()
```

---

## 2. 그래프 생성

```python
plt.bar()
```

또는

```python
plt.pie()
```

---

## 3. Tkinter Canvas 변환

```python
canvas = FigureCanvasTkAgg(
    fig,
    parent
)
```

---

## 4. 화면 표시

```python
canvas.draw()
```

---

## Matplotlib pyplot 방식과 객체 지향 방식 비교

Matplotlib에서는 그래프를 생성하는 방법이 크게 두 가지가 있다.

- pyplot 방식 (`plt`)
- 객체 지향 방식 (`fig`, `ax`)

초기에는 간단한 그래프 생성을 위해 pyplot 방식을 사용할 수 있지만, Tkinter와 같이 여러 화면에서 그래프를 관리하는 경우 객체 지향 방식이 더 적합하다.

---

## plt 방식 vs ax 방식

| 구분 | pyplot 방식 | 객체 지향 방식 |
|---|---|---|
| 방식 | pyplot 방식 | 객체 지향 방식 |
| 대상 | 현재 활성 그래프 | 지정한 ax 객체 |
| 단일 그래프 | 가능 | 가능 |
| 여러 그래프 | 관리 불편 | 적합 |
| Tkinter 같은 UI | 관리 어려움 | 적합 |
| 코드 관리 | 낮음 | 높음 |

---

## 함수 비교

| pyplot 방식 | 객체 지향 방식 |
|---|---|
| `plt.title()` | `ax.set_title()` |
| `plt.xlabel()` | `ax.set_xlabel()` |
| `plt.ylabel()` | `ax.set_ylabel()` |
| `plt.xlim()` | `ax.set_xlim()` |
| `plt.ylim()` | `ax.set_ylim()` |
| `plt.grid()` | `ax.grid()` |

---

## pyplot 방식 예시

```python
plt.title("카테고리별 지출")
plt.xlabel("카테고리")
plt.ylabel("금액")

plt.bar(category, price)
```

현재 활성화된 그래프에 직접 적용하는 방식이다.

---

## 객체 지향 방식 예시

```python
fig, ax = plt.subplots()

ax.set_title("카테고리별 지출")
ax.set_xlabel("카테고리")
ax.set_ylabel("금액")

ax.bar(category, price)
```

생성한 `ax` 객체를 통해
원하는 그래프를 명확하게 제어할 수 있다.

---

## 프로젝트 적용

WeddingMoneyManager에서는

- Tkinter 내부 그래프 표시
- Dashboard 여러 통계 화면
- Excel Report와 동일한 분석 구조 유지

등을 고려하여 객체 지향 방식 사용을 권장한다.

간단한 그래프 하나:

```python
plt.title()
```

사용 가능

하지만 현재 프로젝트처럼:

- Tkinter GUI
- 여러 통계 화면
- Dashboard Card UI
- 여러 Chart 관리

구조에서는:

```python
ax.set_title()
```

방식을 사용하는 것이 적합하다.


---

# 19. 데이터 구조 개선

초기 버전에서는 List Index를 기준으로 데이터를 관리하였다.

문제점:

- 데이터 삭제 시 Index 변경
- 수정 대상 식별 어려움
- 데이터 관리 불안정


개선:

각 데이터에 고유 ID를 추가하였다.

```json
{
  "id": 1,
  "item": "냉장고",
  "price": 2500000
}
```

장점:

- 수정 시 정확한 데이터 접근 가능
- 삭제 시 Index 의존 제거
- 데이터베이스 구조로 변경하기 쉬움

---

# 20. SQLite Migration

초기 버전에서는 JSON 파일(`money.json`)을 이용하여 데이터를 저장하였다.

변경 전:

```text
JSON
 ↓
money.json
 ↓
Python json 모듈
```

문제점:

* 데이터가 증가할수록 검색 및 관리가 어려움
* 조건 검색 및 정렬 기능 구현에 한계
* 데이터 구조 변경 시 전체 파일 수정 필요
* 데이터 접근 코드와 저장 방식이 강하게 연결됨

개선:

SQLite 데이터베이스를 적용하여 데이터 저장 구조를 변경하였다.

변경 후:

```text
SQLite Database
        ↓
   sqlite3 모듈
        ↓
 database/
        ↓
   main.py
```

개선 효과:

* SQL 기반 데이터 조회 가능
* 데이터 CRUD 구조 명확화
* 저장 데이터 관리 안정성 향상
* 향후 모바일 앱 또는 API 서버 구조로 확장 가능한 기반 마련

---

# 21. SQLite Database 기초

SQLite는 별도의 데이터베이스 서버 없이 하나의 파일로 동작하는 관계형 데이터베이스이다.

WeddingMoneyManager에서는 SQLite 데이터베이스 파일인:

```text
wedding.db
```

를 이용하여 지출 데이터와 설정 데이터를 관리한다.

## sqlite3 연결

Python 기본 라이브러리인 sqlite3를 사용한다.

```python
import sqlite3

conn = sqlite3.connect("wedding.db")
cursor = conn.cursor()

conn.commit()
```

## Table 생성

데이터를 저장하기 위해 Table을 생성한다.

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    item TEXT NOT NULL,
    shop TEXT,
    price INTEGER NOT NULL,
    payment TEXT
);
```

## Database 구조

### expenses

지출 내역 저장

| Column   | Type    | Description |
| -------- | ------- | ----------- |
| id       | INTEGER | 고유 ID       |
| date     | TEXT    | 지출 날짜       |
| category | TEXT    | 분류          |
| item     | TEXT    | 항목          |
| shop     | TEXT    | 구매처         |
| price    | INTEGER | 금액          |
| payment  | TEXT    | 결제수단        |

### settings

프로그램 설정값 저장

| Column | Type | Description |
| ------ | ---- | ----------- |
| key    | TEXT | 설정 이름       |
| value  | TEXT | 설정 값        |

### categories

카테고리 저장

| Column | Type    | Description |
| ------ | ------- | ----------- |
| id     | INTEGER | 고유 ID      |
| name   | TEXT    | 카테고리명    |

---

# 22. CRUD (Create Read Update Delete)

데이터베이스 기본 동작은 CRUD 구조로 관리한다.

## Create

데이터 추가

```sql
INSERT INTO expenses
(date, category, item, price)
VALUES (?, ?, ?, ?)
```
### Parameter Binding

SQL Query에 값을 직접 문자열로 넣지 않고 ? Placeholder를 사용한다.

## Read

데이터 조회

```sql
SELECT *
FROM expenses
```

## Update

데이터 수정

```sql
UPDATE expenses
SET price = ?
WHERE id = ?
```

## Delete

데이터 삭제

```sql
DELETE FROM expenses
WHERE id = ?
```

Python 코드에서는 SQL Query를 직접 main.py에서 관리하지 않고, `database.py`에서 담당하도록 분리하였다.

---

# 23. Data Access Layer 분리

기존 구조:

```text
main.py
 |
 ├── 데이터 처리
 ├── JSON 저장
 ├── JSON 불러오기
 └── 화면 처리
```

문제점:

* UI 코드와 데이터 저장 코드가 섞임
* 저장 방식 변경 시 수정 범위 증가

개선 구조:

```text
main.py
   |
   └── database/
          |
          ├── connection.py
          ├── expense.py
          ├── settings.py
          └── category.py
                  |
                  └── SQLite
```

역할 분리:

## main.py

* 화면 구성
* 사용자 입력 처리
* 화면 갱신

## database/

* 데이터 추가
* 데이터 조회
* 데이터 수정
* 데이터 삭제
* 데이터베이스 연결 관리

장점:

* 유지보수 쉬움
* 테스트 용이
* 향후 다른 저장 방식으로 변경 가능
* 향후 API 서버 구조로 확장하기 쉬운 형태로 개선

---

# 24. JSON → SQLite 데이터 Migration

기존 JSON 데이터를 SQLite 데이터베이스로 이전하기 위해 Migration 스크립트를 작성하였다.

구조:

```text
money_backup.json

        ↓

migrate_json_to_sqlite.py

        ↓

wedding.db
```

Migration 과정:

1. JSON 파일 읽기

```python
json.load()
```

2. 기존 데이터 확인

3. SQLite Insert 실행

```sql
INSERT INTO expenses (...)
VALUES (...)
```

4. 데이터 저장

Migration을 별도의 파일로 분리하여 기존 데이터 보존과 테스트가 가능하도록 구성하였다.

---

# 25. 프로젝트 구조 개선

SQLite 적용 이후 기능이 계속 추가되면서 하나의 파일에 여러 역할이 섞이는 문제를 해결하기 위해 프로젝트를 기능별 패키지로 분리하였다.

기존에는 데이터베이스 처리, UI, 부가 기능 등이 하나의 파일에 집중되어 있었지만, 현재는 각 기능의 역할에 따라 패키지를 분리하였다.

```text
WeddingMoneyManager
│
├── main.py
│
├── database/
│   ├── connection.py
│   ├── init_db.py
│   ├── expense.py
│   ├── settings.py
│   └── category.py
│
├── ui/
│   ├── expense_dialog.py
│   ├── statistics_window.py
│   ├── category_window.py
│   ├── settings_window.py
│   └── budget_dialog.py
│
├── utils/
│   ├── csv_export.py
│   └── database_backup.py
│
└── excel/
    ├── excel_export.py
    ├── chart.py
    ├── detail.py
    ├── summary.py
    └── style.py
```

## 역할 분리

### main.py

프로그램의 시작점이며 메인 Dashboard와 사용자 이벤트를 관리한다.

주요 역할:

* 프로그램 실행
* 메인 화면 구성
* 지출 목록 표시
* 검색 및 필터
* Dashboard 갱신
* 각 기능 창 호출
* Callback을 통한 화면 갱신

---

### database/

SQLite 데이터베이스와 직접 통신하는 계층이다.

```text
database/
├── connection.py
├── init_db.py
├── expense.py
├── settings.py
└── category.py
```

#### connection.py

데이터베이스 연결을 관리한다.

```python
def get_connection():
    return sqlite3.connect(DB_PATH)
```

#### init_db.py

프로그램에서 사용하는 테이블을 초기 생성한다.

#### expense.py

지출 데이터 CRUD를 담당한다.

* 지출 추가
* 지출 조회
* 지출 수정
* 지출 삭제

#### settings.py

프로그램 설정값을 관리한다.

현재는 예산을 `settings` 테이블에 저장한다.

```text
key      value
----------------
budget   30000000
```

#### category.py

카테고리 Master Data를 관리한다.

* 카테고리 조회
* 카테고리 추가
* 카테고리 수정
* 카테고리 삭제
* 중복 카테고리 검사
* 사용 중인 카테고리 삭제 방지

---

### ui/

Tkinter 기반 화면을 관리한다.

#### expense_dialog.py

지출 등록 및 수정 창

#### statistics_window.py

통계 및 그래프 화면

#### category_window.py

카테고리 관리 화면

#### settings_window.py

프로그램 설정 화면

* 예산 관리
* 카테고리 관리
* CSV Export
* Database Backup
* Database Restore

#### budget_dialog.py

예산 입력 기능을 별도의 팝업으로 분리하였다.

---

### utils/

프로그램의 부가 기능을 담당한다.

#### csv_export.py

지출 데이터를 CSV 파일로 내보낸다.

#### database_backup.py

SQLite Database의 Backup / Restore를 담당한다.

---

### excel/

Excel Report 생성을 담당한다.

* `excel_export.py` → Excel 생성 흐름
* `detail.py` → 지출 상세 내역
* `summary.py` → 요약 Dashboard
* `chart.py` → 차트
* `style.py` → 셀 스타일

---

## 패키지 분리의 장점

기능별로 파일을 분리하면서 다음과 같은 장점이 생겼다.

* 코드 가독성 향상
* 유지보수성 향상
* 기능별 테스트 용이
* 새로운 기능 추가 시 수정 범위 감소
* UI와 데이터 처리 로직 분리
* 향후 기능 확장에 유리

특히 SQLite 관련 코드를 `database/`로 분리함으로써 UI 코드에서 SQL Query를 직접 처리하지 않도록 구조를 개선하였다.


---

# 26. Build & Deployment

PyInstaller를 이용하여 Python 실행 환경이 없는 Windows 사용자도 사용할 수 있도록 실행 파일 배포 환경을 구성하였다.

WeddingMoneyManager는 단순히 Python 코드를 실행하는 방식에서 벗어나,
사용자가 Python 설치 없이 실행할 수 있는 Windows Desktop Application 형태로 배포하는 것을 목표로 하였다.

---

## PyInstaller 설치

Python 프로젝트를 실행 파일로 변환하기 위해 PyInstaller를 설치한다.

```bash
python -m pip install pyinstaller
```
---

## Build

main.py를 기준으로 실행 파일을 생성한다.

```bash
pyinstaller --onedir --windowed --name WeddingMoneyManager main.py
```
| 옵션         | 설명                       |
| ---------- | ------------------------ |
| --onedir   | 필요한 라이브러리와 파일을 폴더 형태로 생성 |
| --windowed | 콘솔 창 없이 GUI 프로그램 실행      |
| --name     | 생성되는 실행 파일 이름 지정         |

---

## spec 기반 Build
```bash
pyinstaller WeddingMoneyManager.spec
```

또는 기존 Build 결과물을 삭제하고 다시 생성:
```bash
pyinstaller --clean WeddingMoneyManager.spec
```

## WeddingMoneyManager.spec 역할
.spec 파일은 PyInstaller Build 설정 파일이다. 실행 파일 생성 과정에서 필요한 설정을 관리한다.
- 실행 파일 이름
- 아이콘 설정
- hidden import 설정
- 포함할 데이터 파일
- 추가 리소스 설정

## 프로젝트 Build 구조
```text
WeddingMoneyManager
│
├── main.py
│
├── resources
│   └── wedding.db
│
├── icon.ico
│
└── WeddingMoneyManager.spec
```

## Build 과정
```text
Python Source Code
        ↓
WeddingMoneyManager.spec
        ↓
PyInstaller Build
        ↓
WeddingMoneyManager.exe
```

## 주요 설정
- hidden import 관리
- icon 설정
- 데이터 파일 포함
- 배포 환경 테스트

## 배포 결과
Build 완료 후 생성된 실행 파일은 Python 환경이 없는 Windows에서도 실행 가능하다.

```text
WeddingMoneyManager
│
├── WeddingMoneyManager.exe
├── resources
│   └── wedding.db
└── 기타 실행 파일 및 라이브러리
```
이를 통해 Python 개발 환경이 없는 Windows 사용자도 WeddingMoneyManager를 별도의 Python 설치 없이 실행할 수 있도록 배포 환경을 구성하였다.

---

# 27. Project Summary

WeddingMoneyManager는 단순한 GUI 프로그램 제작을 넘어, 실제 사용 가능한 데스크톱 애플리케이션 구조를 목표로 개발하였다.

단순 기능 구현을 넘어 데이터 저장 구조 개선, UI/데이터 계층 분리, 자동화 리포트 생성, 배포 환경 구축까지 실제 서비스 개발 과정과 유사한 흐름으로 프로젝트를 발전시켰다.

적용 기술:

| 영역 | 적용 기술 |
|---|---|
| GUI | Tkinter, ttk |
| Database | SQLite, CRUD |
| Database Design | CRUD, Data Access Layer |
| Architecture | Data Access Layer 분리 |
| Visualization | Matplotlib |
| Excel Automation | openpyxl |
| Deployment | PyInstaller |
| Version Control | Git / GitHub |

---

# 28. SQLite를 이용한 Master Data 관리

WeddingMoneyManager에서는 카테고리를 코드에 하드코딩하지 않고 categories 테이블에서 관리하도록 변경하였다.

기존

ExpenseDialog
↓
values=[...]

현재

ExpenseDialog
↓
database.category.get_category_list()
↓
SQLite

---

# 29. Settings Window와 Callback 구조

설정 창에서 변경한 예산을 메인 Dashboard에 즉시 반영하기 위해 Callback 구조를 적용하였다.

## 문제

예산을 `BudgetDialog`에서 변경하고 Database에 저장하는 것까지는 가능하지만, 이미 열려 있는 `main.py`의 Dashboard 화면은 자동으로 변경되지 않는다.

따라서 예산 변경이 완료되었을 때 메인 화면에 변경 사실을 전달할 필요가 있다.

---

## Callback 구조

전체적인 흐름은 다음과 같다.

```text
main.py
   │
   │ callback 전달
   ▼
SettingsWindow
   │
   │ callback 전달
   ▼
BudgetDialog
   │
   │ 예산 저장 완료
   ▼
callback 실행
   │
   ▼
main.py의 update_budget()
   │
   ▼
Dashboard 갱신
```

main.py에서 Callback을 전달한다.

```python
SettingsWindow(
    window,
    callback=update_budget
)
```

SettingsWindow에서는 전달받은 Callback을 저장한다.

```python
def __init__(self, parent, callback=None):
    super().__init__(parent)

    self.callback = callback
```

BudgetDialog를 열 때 Callback을 다시 전달한다.

```python
BudgetDialog(
    self,
    callback=self.callback
)
```

예산 저장이 완료되면 Callback을 실행한다.

```python
if self.callback:
    self.callback()
```

이를 통해 하위 팝업에서 변경된 데이터를 메인 화면에 전달할 수 있다.

---

# 30. Tkinter 부모-자식 Window 구조

WeddingMoneyManager에서는 여러 개의 팝업 Window를 사용한다.

```text
main.py
  │
  └── SettingsWindow
          │
          └── BudgetDialog
```

`Toplevel`을 사용하면 기존 메인 Window 위에 별도의 창을 생성할 수 있다.

```python
class SettingsWindow(tk.Toplevel):

    def __init__(self, parent, callback=None):
        super().__init__(parent)
```

여기서 `parent`는 해당 팝업을 생성한 부모 Window이다.

---

## Modal Window

Settings Window에서는 메인 화면과 동시에 조작할 수 없도록 Modal 형태로 구성하였다.

```python
self.transient(parent)
self.grab_set()
```

`grab_set()`을 사용하면 사용자가 설정 창을 닫기 전까지 다른 Window의 입력을 제한할 수 있다.

이를 통해 설정 작업 중 실수로 메인 화면의 버튼을 클릭하는 문제를 방지하였다.

---

# 31. Master Data 관리

카테고리와 같이 프로그램에서 반복적으로 사용되는 기준 데이터를 Master Data로 관리할 수 있다.

기존에는 카테고리를 코드에 직접 작성하였다.

```python
values=[
    "예식",
    "가전",
    "가구",
    "신혼여행"
]
```

이 방식은 카테고리를 변경하려면 프로그램 소스 코드를 수정해야 한다는 문제가 있다.

이를 해결하기 위해 `categories` 테이블을 생성하였다.

```text
categories
│
├── id
└── name
```

현재 구조:

```text
CategoryWindow
       ↓
database/category.py
       ↓
SQLite categories
       ↓
ExpenseDialog
```

따라서 사용자가 프로그램에서 직접 카테고리를 추가하거나 수정할 수 있다.

---

## Master Data의 장점

* 프로그램 수정 없이 데이터 변경 가능
* 중복 데이터 방지
* 기준 데이터 중앙 관리
* 다른 기능에서 동일한 데이터 재사용 가능

WeddingMoneyManager에서는 카테고리를 첫 번째 Master Data로 적용하였다.

---

# 32. Database Backup

SQLite는 하나의 `.db` 파일로 데이터를 저장하기 때문에 파일 자체를 복사하여 백업할 수 있다.

Python의 `shutil.copy()`를 사용하였다.

```python
shutil.copy(
    DATABASE_FILE,
    save_path
)
```

전체적인 흐름:

```text
wedding.db
    │
    ▼
사용자가 저장 위치 선택
    │
    ▼
backup_database()
    │
    ▼
백업용 .db 파일 생성
```

사용자가 원하는 위치를 직접 선택할 수 있도록 `filedialog.asksaveasfilename()`을 사용하였다.

---

# 33. Database Restore

Database Restore는 사용자가 선택한 Backup Database를 현재 사용하는 Database로 교체하는 기능이다.

기본적인 흐름:

```text
Backup DB 선택
      ↓
파일 검증
      ↓
복원 확인
      ↓
현재 DB 백업
      ↓
Backup DB → 현재 DB
      ↓
프로그램 재실행
```

복원 전에 현재 DB를 자동으로 백업하여 데이터 손실 가능성을 줄였다.

```python
shutil.copy(
    DATABASE_FILE,
    backup_before_restore
)
```

---

# 34. Database Restore 파일 검증

단순히 `.db` 확장자를 가진 파일이라고 해서 정상적인 WeddingMoneyManager Database라고 볼 수 없다.

예를 들어:

```text
broken.db
```

처럼 실제 SQLite Database가 아닌 파일도 `.db` 확장자를 가질 수 있다.

따라서 Restore 전에 Database의 유효성을 검증하도록 개선하였다.

검증 과정:

```text
사용자가 .db 파일 선택
        ↓
SQLite Database인지 확인
        ↓
필수 Table 존재 여부 확인
        ↓
WeddingMoneyManager Database인지 확인
        ↓
정상인 경우 Restore
```

검증 대상에는 프로그램에서 사용하는 주요 Table이 포함된다.

```text
expenses
settings
categories
```

이를 통해 잘못된 Database를 현재 사용자 Database에 덮어쓰는 문제를 방지하였다.

---

## 잘못된 Database 처리

정상적인 SQLite Database가 아닌 경우:

```text
선택한 파일은 WeddingMoneyManager에서
사용할 수 있는 데이터베이스가 아닙니다.
```

와 같은 안내를 표시하고 Restore를 중단한다.

이를 통해 다음과 같은 상황을 방지할 수 있다.

* 잘못된 `.db` 파일 선택
* SQLite가 아닌 파일 선택
* 다른 프로그램의 SQLite Database 선택
* 필수 Table이 없는 Database 선택

---

# 35. CSV Export

지출 데이터를 다른 프로그램에서도 사용할 수 있도록 CSV Export 기능을 추가하였다.

```text
SQLite
  ↓
get_all_expenses()
  ↓
csv.writer
  ↓
CSV File
```

한글 데이터를 Excel에서 열었을 때 깨지는 문제를 방지하기 위해 `utf-8-sig` 인코딩을 사용하였다.

```python
with open(
    file_path,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:
```

이를 통해 Windows 환경에서 Excel로 CSV 파일을 열 때 한글이 정상적으로 표시되도록 처리하였다.

---

# 36. Resource Database와 사용자 Database 분리

PyInstaller로 프로그램을 배포하면서 초기 Database와 사용자가 실제로 사용하는 Database를 분리하였다.

배포에 포함되는 Database:

```text
resources/
└── wedding.db
```

이 파일은 테이블 구조와 기본 설정을 제공하기 위한 **초기 템플릿 Database**이다.

프로그램 최초 실행 시 이 템플릿을 기반으로 사용자 Database를 생성한다.

```text
배포용 초기 DB
resources/wedding.db
        ↓
최초 실행
        ↓
사용자 DB 생성
        ↓
사용자 데이터 저장
```

이렇게 분리하면 프로그램 업데이트나 재배포 시 배포용 초기 Database와 사용자의 실제 데이터를 구분할 수 있다.

---

# 37. PyInstaller와 Resource Path

Python으로 실행할 때와 PyInstaller로 빌드한 exe로 실행할 때 파일 경로가 달라질 수 있다.

따라서 실행 환경을 고려하여 Resource 경로와 사용자 Database 경로를 구분하였다.

개발 환경:

```text
프로젝트/
└── resources/
    └── wedding.db
```

PyInstaller 실행 환경에서는 포함된 리소스가 `_internal` 영역에 위치할 수 있다.

```text
WeddingMoneyManager/
├── WeddingMoneyManager.exe
└── _internal/
    └── wedding.db
```

따라서 초기 템플릿 Database와 실제 사용자 Database의 위치를 분리하여 관리하는 것이 중요하다.
