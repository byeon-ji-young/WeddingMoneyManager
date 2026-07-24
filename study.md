# 📚 Python Tkinter 신혼 자금 관리 Dashboard 개발 정리 노트

Tkinter GUI 프레임워크와 Matplotlib 시각화 라이브러리를 활용해 **실제 동작하는 자금 관리 대시보드 애플리케이션**을 제작하면서 학습한 개념을 정리한 문서입니다.

---

## 📌 1. 전체 프로그램 아키텍처

```text
[ 사용자 입력 및 조작 ]
        │
        ├── (1) 지출 내역 입력 (DateEntry, Combobox, Entry)
        ├── (2) 검색 및 정렬 (Entry, Header Click)
        └── (3) 예산 변경 / 데이터 수정 및 삭제
        │
        ▼
[ 이벤트 처리 함수 (Functions) ]
        │
        ├── add_money() / update_money() / delete_money()
        ├── search_money() / sort_column()
        └── show_bar_chart() / show_pie_chart()
        │
        ▼
[ 메모리 데이터 관리 (Global State) ]
        │
        ├── budget (int)
        └── money_data (List of Dicts)
        │
        ├──▶ [ GUI 갱신 (update_total, display_data) ]
        └──▶ [ 파일 입출력 (save_data ⇄ money.json) ]
```
--- 

## 📦 2. 라이브러리 (Import) 및 역할

| 라이브러리 / 모듈 | 주요 역할 및 사용 목적 |
| :--- | :--- |
| `tkinter (as tk)` | 기본 GUI 창 생성 및 레이아웃 위젯 (Frame, Label, Button, Entry) 제공 |
| `tkinter.messagebox` | 사용자 경고, 에러 알림, 삭제 확인 등의 대화상자(Modal Window) 출력 |
| `tkinter.ttk` | 개선된 테마 기반 위젯 (Combobox, Treeview, Scrollbar, Style) 제공 |
| `tkcalendar.DateEntry` | 달력 팝업을 지원하는 날짜 선택 위젯 |
| `json` | 예산 및 지출 내역 데이터를 로컬 파일(`money.json`)로 저장/로드 |
| `datetime` | 오늘 날짜 가져오기 및 날짜 문자열 포맷팅 |
| `matplotlib.pyplot` | 지출 데이터를 기반으로 막대그래프 및 도넛형 원형그래프 생성 |

---

## 🎨 3. GUI 레이아웃 & 위젯 배치 기법

### 3.1 배치 관리자 (Geometry Managers)
* **`pack()`**: 위젯을 상/하/좌/우 방향으로 유연하게 추가할 때 사용 (대형 틀 배치에 유리)
  * `fill="x"`: 가로 방향으로 영역을 채움
  * `expand=True`: 부모 창 크기가 커질 때 남는 공간을 배분받음
  * `anchor="w"`: 위젯 내부 정렬 (w: 서쪽/왼쪽, e: 동쪽/오른쪽, n: 북쪽/위)
* **`grid()`**: 정교한 바둑판 배열(행`row`, 열`column`) 형태로 위젯을 입력 폼 내부 등에 배치
  * `sticky="ew"`: 셀 내부에서 좌우로 늘어나도록 밀착시킴
  * `columnconfigure(col, weight=1)`: 특정 열이 창 크기 변화에 맞춰 늘어나는 비율 설정

### 3.2 핵심 고급 위젯
* **`ttk.Treeview`**: 단순히 한 줄씩 보여주는 `Listbox`와 달리, 여러 컬럼(날짜, 분류, 항목, 금액)을 갖는 표 형태로 데이터를 표시
* **`ttk.Combobox`**: 드롭다운 메뉴를 제공하여 입력 오류 방지 (`values=[...]`)
* **`tkcalendar.DateEntry`**: 사용자 입력을 간편하게 만드는 팝업 달력 위젯

---

## 💡 4. 핵심 파이썬 문법 및 응용 개념

### 4.1 데이터 구조 (JSON & Python)
메모리 상에서는 **딕셔너리를 포함한 리스트** 형태로 데이터를 관리합니다.
```python
{
    "budget": 30000000,
    "money_data": [
        {"date": "2026-05-10", "category": "가전", "item": "냉장고", "price": 2500000},
        {"date": "2026-05-12", "category": "예식장", "item": "계약금", "price": 5000000}
    ]
}
```
### 4.2 파일 입출력 및 예외 처리 (try-except)
```python
def load_data():
    global money_data, budget
    try:
        with open("money.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # 예전 버전 JSON 데이터(리스트 형식)와의 호환성 예외 처리
            if isinstance(data, list):
                money_data = data
                budget = 30000000
            else:
                budget = data.get("budget", 30000000) # Safety Get
                money_data = data.get("money_data", [])
    except FileNotFoundError:
        money_data = [] # 파일이 없으면 초기 상태 유지
```

### 4.3 데이터 정렬 (sort & lambda)
``` python
def sort_column(column):
    # sort_reverse 딕셔너리를 통해 현재 상태 반전
    money_data.sort(key=lambda money: money[column], reverse=sort_reverse[column])
    sort_reverse[column] = not sort_reverse[column]
    display_data() # 정렬된 데이터로 화면 재갱신
```

### 4.4 데이터 시각화 및 클로저(Closure) 활용
``` python
def make_autopct(values):
    def my_autopct(percent):
        total = sum(values)
        price = int(total * percent / 100)
        if percent < 5:
            return f"{percent:.1f}%" # 비중이 작으면 퍼센트만 표시
        else:
            return f"{percent:.1f}%\n({price:,}원)" # 퍼센트와 금액 함께 표시
    return my_autopct
```

---

## 🔄 5. 주요 이벤트 흐름 (Event Flow)

### 5.1 지출 항목 추가 / 수정
1. 사용자가 폼 필드 입력 후 `➕ 추가` 또는 `✏ 수정` 버튼 클릭
2. `get()` 함수로 날짜, 카테고리, 항목명, 금액 입력값 추출
3. `int(price)` 예외 검증을 거쳐 `money_data` 리스트 업데이트
4. `save_data()` ➔ `display_data()` ➔ `update_total()` 연속 실행으로 상태 동기화
5. `refresh_input_entry()`를 호출하여 입력 폼 초기화

### 5.2 지출 항목 삭제
1. `money_list.selection()`으로 `Treeview`에서 선택된 행의 Index 확인
2. `messagebox.askyesno()` 모달창으로 사용자 재확인
3. `money_data.pop(index)`로 메모리 데이터 제거 및 화면/파일 업데이트

---

## 📑 6. Tkinter vs Java Swing 위젯 대응표

| 목적 | Tkinter (Python) | Java Swing (Java) |
| :--- | :--- | :--- |
| 단순 텍스트 레이블 | `tk.Label` | `JLabel` |
| 한 줄 텍스트 입력창 | `tk.Entry` | `JTextField` |
| 선택 항목 드롭다운 | `ttk.Combobox` | `JComboBox` |
| 다중 컬럼 표(테이블) | `ttk.Treeview` | `JTable` |
| 클릭 버튼 | `tk.Button` | `JButton` |
| 레이아웃 컨테이너 | `tk.Frame` | `JPanel` |