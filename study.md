# tkinter 신혼 자금 관리 프로그램 만들기

## 전체 흐름

이번 프로그램은 tkinter를 이용해서 만든 간단한 가계부 프로그램이다.

기능:

- 항목 입력
- 금액 입력
- 지출 추가
- 지출 삭제
- 총 지출 계산
- JSON 파일 저장
- 프로그램 실행 시 기존 데이터 불러오기

사용 기술:

- tkinter → GUI 화면 제작
- json → 데이터 저장 및 불러오기


---

# import 영역

```python
import tkinter as tk
from tkinter import messagebox
import json
```

## import tkinter as tk

- tkinter GUI 라이브러리 가져오기
- `as tk` : 별명 지정

이후 tkinter 기능을 사용할 때

```python
tk.Label()
tk.Button()
tk.Entry()
```

처럼 사용할 수 있다.


---

## from tkinter import messagebox

- tkinter 내부의 메시지 창 기능 가져오기

사용 예:

```python
messagebox.showwarning(
    "입력 오류",
    "항목과 금액을 입력하세요."
)
```

결과:

- 경고창 표시


---

## import json

JSON 파일을 다루기 위한 라이브러리

사용 목적:

- 프로그램 종료 후 데이터 유지
- 입력한 지출 내역 저장


---

# 데이터 저장 변수

```python
money_data = []
```

## 리스트(List)

- 지출 데이터를 저장하는 공간

예:

```python
[
    {
        "item": "식비",
        "price": 50000
    },
    {
        "item": "가구",
        "price": 1000000
    }
]
```


---

# 메인 윈도우 생성

```python
window = tk.Tk()
```

- 프로그램의 메인 창 생성

Java 기준:

```java
new JFrame()
```

과 비슷한 개념


---

# 함수 영역


# add_money()

## 지출 추가 함수

```python
def add_money():
```

역할:

- 입력값 가져오기
- 데이터 검증
- 리스트 추가
- 총 금액 업데이트
- JSON 저장


---

## 입력값 가져오기

```python
item = item_entry.get()
price = price_entry.get()
```

## Entry.get()

- Entry 입력창 안의 값을 가져오는 함수


예:

입력:

```
가구
500000
```

결과:

```python
item = "가구"
price = "500000"
```


---

# 입력값 검사

```python
if item == "" or price == "":
```

빈 값인지 확인

빈 값이면:

```python
messagebox.showwarning()
```

으로 경고창 표시


---

# 숫자 변환

```python
price = int(price)
```

Entry에서 가져온 값은 문자열(str)

예:

```python
"50000"
```

을

```python
50000
```

숫자로 변환


---

## try / except

```python
try:
    price = int(price)

except:
```

예외 처리

잘못된 입력:

```
abc
```

같은 값이 들어오면 오류 발생

→ 프로그램 종료 방지


---

# Listbox에 데이터 추가

```python
money_list.insert(
    tk.END,
    f"{item} - {price}원"
)
```

## tk.END

- 리스트 마지막 위치 의미


예:

기존:

```
식비 - 50000원
```

추가:

```
가구 - 1000000원
```

결과:

```
식비 - 50000원
가구 - 1000000원
```


---

# f-string

```python
f"{item} - {price}원"
```

문자열 안에 변수를 넣는 방법


예:

```python
name="철수"

f"{name}님"
```

결과:

```
철수님
```


---

## f-string 포맷

소수점:

```python
f"{price:.2f}"
```

퍼센트:

```python
f"{rate:.0%}"
```


---

# dictionary 저장

```python
money_data.append({
    "item": item,
    "price": price
})
```


## Dictionary(딕셔너리)

Key와 Value 형태의 데이터


예:

```python
{
    "item": "식비",
    "price": 50000
}
```


사용:

```python
money["price"]
```

결과:

```
50000
```


---

# 입력창 초기화

```python
item_entry.delete(0, tk.END)
price_entry.delete(0, tk.END)
```


## Entry.delete()

입력창 내용 삭제


```python
delete(0, tk.END)
```

의미:

- 0번째 글자부터
- 마지막 글자까지 삭제


---

# update_total()

## 총 지출 계산 함수


```python
def update_total():
```

역할:

- 저장된 모든 금액 합산
- 화면에 표시


---

## 반복문으로 합계 계산

```python
for money in money_data:
    total += money["price"]
```


예:

```python
money_data=[
 {"price":10000},
 {"price":20000}
]
```

결과:

```
total = 30000
```


---

## config()

```python
total_label.config(
    text=f"총 지출 : {total:,}원"
)
```


이미 만들어진 위젯의 설정 변경


예:

기존:

```
총 지출 : 0원
```

변경:

```
총 지출 : 30,000원
```


---

# delete_money()

## 선택한 지출 삭제


```python
selected = money_list.curselection()
```


## curselection()

현재 선택된 Listbox 위치 반환


예:

두 번째 항목 선택

결과:

```python
(1,)
```


---

## 삭제

```python
money_data.pop(index)
```

리스트에서 해당 위치 데이터 제거


```python
money_list.delete(index)
```

화면 리스트에서도 제거


---

# save_data()

## JSON 파일 저장


```python
with open(
    "money.json",
    "w",
    encoding="utf-8"
)
```

파일 열기


## open()

파일을 여는 함수


모드:

| 모드 | 의미 |
|---|---|
| r | 읽기 |
| w | 새로 쓰기 |
| a | 이어 쓰기 |


---

## with

파일 자동 관리


일반 방식:

```python
file=open()

file.close()
```

with 사용:

```python
with open() as file:
```

자동으로 닫힘


---

# json.dump()

```python
json.dump(
    money_data,
    file,
    ensure_ascii=False,
    indent=4
)
```


Python 데이터를 JSON 파일로 저장


---

## ensure_ascii=False

한글 저장 유지


True:

```json
"\uc2dd\ube44"
```


False:

```json
"식비"
```


---

## indent=4

JSON 파일 보기 좋게 들여쓰기


---

# load_data()

## 저장된 데이터 불러오기


```python
json.load(file)
```


JSON 데이터를 Python 객체로 변환


---

## global

```python
global money_data
```


함수 밖의 변수를 함수 안에서 변경하기 위해 사용


---

# FileNotFoundError

```python
except FileNotFoundError:
```

파일이 없을 때 발생하는 오류


예:

처음 실행하면

```
money.json 없음
```

→ 빈 리스트 생성


---

# display_data()

## 저장된 데이터 화면 표시


```python
for money in money_data:
```

저장된 데이터를 하나씩 꺼내서


```python
money_list.insert()
```

Listbox에 출력


---

# 화면 구성 영역


# 창 설정

```python
window.title(
"💒 신혼 자금 관리"
)
```

창 제목 설정


---

```python
window.geometry(
"800x600"
)
```


창 크기 설정


형식:

```
가로x세로
```


---

# tkinter 위젯


## Label

```python
tk.Label()
```

글자를 표시하는 위젯


예:

```
항목
금액
총 지출
```


---

## Entry

```python
tk.Entry()
```

사용자가 입력하는 공간


예:

```
[ 식비      ]
[ 50000     ]
```


---

## Button

```python
tk.Button()
```

버튼 생성


예:

```
추가
삭제
```


---

## Listbox

```python
tk.Listbox()
```

목록 표시


예:

```
식비 - 50000원
가구 - 100000원
```


---

# 위젯 배치


## grid()

```python
widget.grid(
row=0,
column=0
)
```


행(row), 열(column) 기준 배치


예:

```
        0열        1열

0행     항목       입력창

1행     금액       입력창

2행     삭제       추가
```


---

# columnspan

```python
columnspan=2
```


두 개의 열을 합침


예:

```
|       총 지출       |
```


---

# Button command


```python
command=add_money
```


버튼 클릭 시 함수 실행


주의:

```python
command=add_money()
```

하면 프로그램 시작할 때 바로 실행됨


---

# 프로그램 실행


```python
load_data()

display_data()

update_total()
```


순서:

1. 저장된 데이터 불러오기
2. 화면에 표시
3. 총 금액 계산


---

# mainloop()

```python
window.mainloop()
```


## 이벤트 루프 시작


역할:

- 창 유지
- 버튼 클릭 감지
- 입력 처리


프로그램은 mainloop 안에서 계속 대기한다.


---

# 최종 프로그램 구조


```
tkinter GUI
    |
    |
사용자 입력
    |
    |
add_money()
    |
    |
money_data 저장
    |
    |
save_data()
    |
    |
money.json 저장


프로그램 시작

load_data()
    |
display_data()
    |
update_total()
```


---

# 이번 실습 핵심 개념

- tkinter 기본 GUI 제작
- 위젯(Label, Entry, Button, Listbox)
- grid 배치
- 함수와 이벤트 연결
- JSON 데이터 저장
- 파일 입출력
- 예외 처리(try/except)
- 리스트와 딕셔너리 활용

| 목적          | Tkinter  | Java Swing   |
| ----------- | -------- | ------------ |
| 그냥 보여주는 글자  | `Label`  | `JLabel`     |
| 사용자가 입력하는 칸 | `Entry`  | `JTextField` |
| 여러 줄 입력     | `Text`   | `JTextArea`  |
| 버튼          | `Button` | `JButton`    |
