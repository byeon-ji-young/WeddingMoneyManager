# 💍 WeddingMoneyManager

> **Python Tkinter를 이용해 개발한 신혼 자금 관리 데스크톱 애플리케이션**

결혼 준비 과정에서 발생하는 **예식, 혼수, 가전·가구, 생활용품, 신혼여행** 등의 다양한 지출을 체계적으로 관리하기 위해 개발한 개인 프로젝트입니다.

예산 설정부터 지출 내역 관리, 검색 및 필터링, Dashboard를 통한 예산 현황 확인, Excel Report 생성을 통한 지출 분석까지 실제 사용을 고려하여 구현했습니다.

---

# 📌 프로젝트 소개

결혼 준비는 짧은 기간 동안 많은 비용이 발생하기 때문에 체계적인 관리가 필요합니다.

WeddingMoneyManager는 이러한 비용을 직접 관리하기 위해 개발한 프로그램으로, 단순한 가계부를 넘어 **예산 관리와 지출 분석 기능을 제공하는 데스크톱 애플리케이션**입니다.

이 프로젝트를 통해 Python GUI 프로그래밍(Tkinter), JSON 데이터 관리, 이벤트 처리, 객체 지향 설계, 모듈 분리, 데이터 시각화, Excel 자동화를 학습하고 적용했습니다.

---

# ✨ 주요 기능

## 💰 비용 관리

* [x] 총 예산 설정
* [x] 지출 내역 등록
* [x] 지출 내역 수정
* [x] 지출 내역 삭제
* [x] JSON 자동 저장 및 불러오기

---

## 📋 지출 목록 관리

* [x] Treeview 기반 목록 출력
* [x] 날짜 / 분류 / 항목 / 구매처 / 금액 / 결제수단 표시
* [x] 컬럼 클릭 정렬 (오름차순 / 내림차순)
* [x] 고유 ID 기반 데이터 관리
* [x] 수정 후 선택 행 유지
* [x] 추가 후 등록한 행 자동 선택

---

## 🔍 검색 및 필터

* [x] 항목명 검색
* [x] 구매처 검색
* [x] 카테고리 필터
* [x] 결제수단 필터
* [x] 검색 조건 초기화

---

## 📊 Dashboard

* [x] 총 예산 Card 표시
* [x] 현재 지출 Card 표시
* [x] 남은 금액 Card 표시
* [x] 예산 사용률 ProgressBar
* [x] 예산 사용률 상태 표시
* [x] 최근 지출 TOP 5 표시
* [x] 카테고리별 지출 분석
* [x] 결제수단별 지출 분석
* [x] Matplotlib 기반 데이터 시각화

---

## 📈 Excel Report

* [x] Excel 리포트 자동 생성
* [x] Summary 대시보드 시트 생성
* [x] Detail 지출 내역 시트 생성
* [x] 예산 사용률 카드 표시
* [x] 카테고리별 지출 분석
* [x] 결제수단별 지출 분석
* [x] 최근 지출 TOP 5 표시
* [x] 카테고리별 BarChart 생성
* [x] 월별 지출 LineChart 생성

---

### In Progress
- [ ] SQLite 데이터베이스 적용

--- 

### Planned
- [ ] 데이터 백업 기능
- [ ] 검색 기능 개선
- [ ] 배포 버전 제작

---

# 🛠 기술 스택

| 구분              | 기술                 |
| --------------- | ------------------ |
| Language        | Python 3           |
| GUI             | Tkinter, ttk       |
| Data            | JSON               |
| Excel           | openpyxl           |
| Chart           | openpyxl.chart, Matplotlib |
| Visualization   | Matplotlib         |
| Calendar        | tkcalendar         |
| Development     | Visual Studio Code |
| Version Control | Git / GitHub       |

---

# 📁 프로젝트 구조

```text
WeddingMoneyManager
│
├── main.py                    # 메인 실행 파일
├── expense_dialog.py          # 지출 등록 / 수정 팝업
├── excel_export.py            # Excel Report 생성 관리
├── statistics.py              # 통계 팝업
│
├── excel
│   ├── chart.py               # Excel 차트 생성
│   ├── detail.py              # 상세 지출 내역 시트 생성
│   ├── summary.py             # Summary 대시보드 생성
│   └── styles.py              # Excel 스타일 관리
│
├── money.json                 # 데이터 저장 파일
├── README.md                  # 프로젝트 소개
├── development_log.md         # 개발 일지
├── study.md                   # Python / Tkinter 학습 노트
└── requirements.txt           # 패키지 목록
```

---

# ⚙ 실행 방법

## 1. 저장소 Clone

```bash
git clone https://github.com/username/WeddingMoneyManager.git
cd WeddingMoneyManager
```

## 2. 가상환경 생성

```bash
python -m venv venv
```

## 3. 가상환경 활성화

### Windows (PowerShell)

```bash
.\venv\Scripts\Activate.ps1
```

### Windows (CMD)

```bash
.\venv\Scripts\activate.bat
```

## 4. 패키지 설치

```bash
pip install -r requirements.txt
```

## 5. 프로그램 실행

```bash
python main.py
```

---

# 💾 데이터 구조

```json
{
  "budget": 30000000,
  "money_data": [
    {
      "id": 1,
      "date": "2026-07-28",
      "category": "가전",
      "item": "냉장고",
      "shop": "삼성스토어",
      "price": 2500000,
      "payment": "신용카드"
    }
  ]
}
```

---

# 📷 화면

추후 실행 화면 추가 예정

* 메인 Dashboard
* 지출 등록 / 수정 팝업
* Excel Summary Report
* 지출 상세 내역

---

# 🗺 Roadmap

## v0.9.0 SQLite Migration

* [ ] SQLite 데이터베이스 적용
* [ ] JSON 저장 방식 제거
* [ ] DB 기반 CRUD 구조 변경
* [ ] 데이터 접근 계층 분리

## Future

* [ ] 검색 결과 건수 표시
* [ ] CSV 내보내기
* [ ] 데이터 백업 및 복원
* [ ] 사용자 설정 기능 추가

---

# 📦 Version History

| Version | Description                                                                          |
| ------- | ------------------------------------------------------------------------------------ |
| v0.5.0 | 첫 번째 공식 Release / Dashboard UI 개선 / 검색·필터 기능 추가 / ExpenseDialog 분리 / 고유 ID 기반 데이터 관리 |
| v0.6.0 | Excel Report 기능 추가 / openpyxl 기반 Summary·Detail 시트 생성 / 지출 분석 Dashboard / 차트 기능 구현 |
| v0.7.0 | Dashboard UI 완성 / Card UI 적용 / 예산·지출·잔액 표시 / ExpenseDialog UI 개선 / 프로젝트 구조 정리 |
| v0.8.0 | 통계창 완성 / 최근 지출 TOP5 추가 / 버튼 및 레이아웃 개선 / 그래프 디자인 마무리 |

---

# 📚 Documentation

프로젝트 개발 과정과 학습 내용은 아래 문서에 정리되어 있습니다.

* **development_log.md** : 개발 일지
* **study.md** : Python / Tkinter / openpyxl 학습 노트

---

# 👤 Developer

**Jiyoung Byeon**

WeddingMoneyManager는 결혼 준비 과정에서 발생하는 실제 지출 데이터를 관리하기 위해 개발한 개인 프로젝트입니다.

단순한 기능 구현을 넘어 Python GUI 프로그래밍(Tkinter), JSON 데이터 관리, 이벤트 처리, 객체 지향 설계, 모듈 분리, 데이터 시각화(Matplotlib), Excel 자동화(openpyxl) 등 실제 애플리케이션 개발 과정에서 필요한 기술을 학습하고 적용했습니다.