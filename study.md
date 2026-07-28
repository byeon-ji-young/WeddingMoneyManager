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

Key : Value 형태의 자료구조

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

한 줄 함수

```python
lambda x:x+1
```

예시

```python
command=lambda: search_money()
```

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

행 추가

```python
insert()
```

행 삭제

```python
delete()
```

전체 삭제

```python
delete(*tree.get_children())
```

선택 행

```python
selection()
```

선택

```python
selection_set()
```

포커스

```python
focus()
```

스크롤 이동

```python
see()
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

- display_data()
- update_total()
- save_data()
- load_data()
- search_money()
- sort_column()
- animate_progress()
- update_budget()

각 함수의 역할은 main.py 주석 참고