# 📚 Python & Tkinter Study Note

> WeddingMoneyManager 프로젝트를 만들면서 학습한 Python, Tkinter 문법 및 개념 정리

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

주로 Tkinter에서 버튼 클릭이나 이벤트 처리 시
함수의 실행을 나중으로 미루거나 인자를 전달할 때 사용한다.

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

# 14. 프로젝트에서 자주 사용하는 함수

- display_data() → Treeview 화면 갱신
- update_total() → 총 지출/예산 계산
- save_data() → JSON 저장
- load_data() → JSON 불러오기
- search_money() → 검색 기능
- sort_column() → 컬럼 정렬
- animate_progress() → ProgressBar 애니메이션
- update_budget() → 예산 변경

※ 자세한 구현 내용은 main.py의 각 함수 주석 참고

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

WeddingMoneyManager의 화면 개선 과정에서
기본 Tkinter 위젯만 사용하는 방식에서 벗어나
ttk.Style을 활용하여 UI 스타일을 관리하였다.

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

Tkinter 기본 디자인 대신
ttk Theme을 적용할 수 있다.

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

기존 Treeview 중심 화면에서
사용자가 중요한 정보를 빠르게 확인할 수 있도록
Dashboard 형태의 UI로 개선하였다.

주요 구성:

- 예산 Card
- 총 지출 Card
- 잔액 Card
- 예산 사용률 표시
- 지출 분석 Chart
- 최근 지출 TOP 5


## Card UI

Tkinter에는 기본 Card 위젯이 없기 때문에
Frame과 Label을 조합하여 직접 구현하였다.

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

Matplotlib 그래프를
Tkinter 화면 내부에 표시하기 위해
FigureCanvasTkAgg를 사용하였다.

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

초기에는 간단한 그래프 생성을 위해 pyplot 방식을 사용할 수 있지만,
Tkinter와 같이 여러 화면에서 그래프를 관리하는 경우
객체 지향 방식이 더 적합하다.

---

## plt 방식 vs ax 방식

| 구분 | pyplot 방식 | 객체 지향 방식 |
|---|---|---|
| 방식 | pyplot 방식 | 객체 지향 방식 |
| 대상 | 현재 활성 그래프 | 지정한 ax 객체 |
| 단일 그래프 | 가능 | 가능 |
| 여러 그래프 | 관리 불편 | 적합 |
| Tkinter 같은 UI | 비추천 | 추천 |
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

초기에는 Treeview Index를 기준으로
데이터를 관리하였다.

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

기존에는 JSON 파일(`money.json`)을 이용하여 데이터를 저장하였다.

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
 database.py
        ↓
   main.py
```

개선 효과:

* SQL 기반 데이터 조회 가능
* 데이터 CRUD 구조 명확화
* 저장 데이터 관리 안정성 향상
* 향후 Flutter 앱 연동을 고려한 구조 마련

---

# 21. SQLite Database 기초

SQLite는 별도의 데이터베이스 서버 없이
하나의 파일로 동작하는 관계형 데이터베이스이다.

WeddingMoneyManager에서는:

```text
wedding.db
```

파일을 생성하여 데이터를 저장한다.

## sqlite3 연결

Python 기본 라이브러리인 sqlite3를 사용한다.

```python
import sqlite3

conn = sqlite3.connect("wedding.db")
cursor = conn.cursor()
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

Python 코드에서는 SQL Query를 직접 main.py에서 관리하지 않고,
`database.py`에서 담당하도록 분리하였다.

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
 └── database.py
          |
          └── SQLite
```

역할 분리:

## main.py

* 화면 구성
* 사용자 입력 처리
* 화면 갱신

## database.py

* 데이터 추가
* 데이터 조회
* 데이터 수정
* 데이터 삭제
* 데이터베이스 연결 관리

장점:

* 유지보수 쉬움
* 테스트 용이
* 향후 다른 저장 방식으로 변경 가능
* Flutter 앱 API 서버 구조로 확장하기 쉬움

---

# 24. JSON → SQLite 데이터 Migration

기존 JSON 데이터를 SQLite 데이터베이스로 이전하기 위해
Migration 스크립트를 작성하였다.

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

Migration을 별도의 파일로 분리하여
기존 데이터 보존과 테스트가 가능하도록 구성하였다.

---

# 25. 프로젝트 구조 개선

SQLite 적용 이후 프로젝트 구조:

```text
main.py
 |
 ├── UI 처리

database.py
 |
 ├── SQLite 연결
 ├── CRUD 처리

migrate_json_to_sqlite.py
 |
 └── 기존 JSON 데이터 이전
```

저장 방식과 화면 로직을 분리하면서
프로젝트가 단순한 GUI 프로그램에서
확장 가능한 애플리케이션 구조로 개선되었다.
