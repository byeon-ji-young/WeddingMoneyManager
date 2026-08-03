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