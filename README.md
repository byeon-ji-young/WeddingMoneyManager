# 💍 WeddingMoneyManager

> **Python Tkinter를 이용해 개발한 신혼 자금 관리 데스크톱 애플리케이션**

## 📦 Download

Windows 환경에서는 PyInstaller로 빌드된 실행 파일(`WeddingMoneyManager.exe`)을 통해 사용할 수 있습니다.

> Release 페이지에서 최신 버전을 다운로드할 수 있습니다.

--- 

결혼 준비 과정에서 발생하는 **예식, 혼수, 가전·가구, 생활용품, 신혼여행** 등의 다양한 지출을 체계적으로 관리하기 위해 개발한 개인 프로젝트입니다.

예산 설정부터 지출 내역 관리, 검색 및 필터링, Dashboard를 통한 예산 현황 확인, Excel Report 생성을 통한 지출 분석까지 실제 사용을 고려하여 구현했습니다.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)
![License](https://img.shields.io/badge/License-MIT-orange)

---

# 📌 프로젝트 소개

결혼 준비는 짧은 기간 동안 많은 비용이 발생하기 때문에 체계적인 관리가 필요합니다.

WeddingMoneyManager는 이러한 비용을 직접 관리하기 위해 개발한 프로그램으로, 단순한 가계부를 넘어 **예산 관리와 지출 분석 기능을 제공하는 데스크톱 애플리케이션**입니다.

이 프로젝트를 통해 Python GUI 프로그래밍(Tkinter), SQLite 데이터베이스, 이벤트 처리, 객체 지향 설계, 모듈 분리, 데이터 시각화(Matplotlib), Excel 자동화(openpyxl), Windows 실행 파일 배포(PyInstaller)를 학습하고 적용했습니다.

---

# ✨ 주요 기능

## 💰 비용 관리

* [x] 총 예산 설정
* [x] 지출 내역 등록
* [x] 지출 내역 수정
* [x] 지출 내역 삭제
* [x] SQLite 데이터베이스 기반 데이터 관리

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

# 🛠 기술 스택

| 구분              | 기술                 |
| --------------- | ------------------ |
| Language        | Python 3           |
| GUI             | Tkinter, ttk       |
| Database        | SQLite  (sqlite3)  |
| Excel           | openpyxl           |
| Chart           | openpyxl.chart, Matplotlib |
| Visualization   | Matplotlib         |
| Calendar        | tkcalendar         |
| Development     | Visual Studio Code |
| Version Control | Git / GitHub       |
| Build           | PyInstaller        |

---

# 📁 프로젝트 구조

```text
WeddingMoneyManager
│
├── main.py
├── database.py
├── database_backup.py
├── expense_dialog.py
├── statistics_window.py
├── excel_export.py
├── csv_export.py
├── migrate_json_to_sqlite.py
│
├── sql/
│   ├── init.sql
│
├── excel/
│   ├── chart.py
│   ├── detail.py
│   ├── summary.py
│   └── style.py
│
├── backup/
│   ├── app.py
│   ├── main_backup.py
│   └── money_backup.json
│
├── images/
│   ├── main.png
│   ├── expense_dialog.png
│   ├── excel_export_1.png
│   ├── excel_export_2.png
│   ├── statistics_1.png
│   └── statistics_2.png
│
├── resources
│   └── wedding.db            # 배포용 초기 템플릿 DB
│
├── icon.ico
├── WeddingMoneyManager.spec
│
├── README.md
├── development_log.md
├── study.md
└── requirements.txt
```
`resources/wedding.db`는 배포용 초기 템플릿 DB이며, 실행 후 생성되는 사용자 데이터 DB는 별도로 관리됩니다.

---

# ⚙ 실행 방법

## 1. 저장소 Clone

```bash
git clone https://github.com/byeon-ji-young/WeddingMoneyManager.git
```

## 2. 가상환경 생성

```bash
python -m venv .venv
```

## 3. 가상환경 활성화

### Windows (PowerShell)

```bash
.\.venv\Scripts\Activate.ps1
```

### Windows (CMD)

```bash
.\.venv\Scripts\activate.bat
```

## 4. 패키지 설치

```bash
cd WeddingMoneyManager

python -m pip install -r requirements.txt
```

## 5. 프로그램 실행

```bash
python main.py
```

---

## Windows 실행 파일

Windows 환경에서는 빌드된 실행 파일을 통해 프로그램을 사용할 수 있습니다.

```text
dist/
└── WeddingMoneyManager/
    ├── WeddingMoneyManager.exe
    └── _internal/
        └── wedding.db (초기 템플릿 DB)
```
실행 시 포함된 초기 DB(`_internal/wedding.db`)는 초기 데이터 구조 제공용으로 사용됩니다.

이후 프로그램에서 생성되는 데이터는 사용자 DB에서 관리되어, 프로그램 업데이트 및 재배포 시 기존 데이터를 유지할 수 있습니다.

## Build (Developer)

PyInstaller spec 파일을 이용하여 Windows 실행 파일을 생성합니다.

```bash
pyinstaller WeddingMoneyManager.spec
```


---

# 💾 Database Schema

### expenses

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | 지출 ID (PK) |
| date | TEXT | 지출 날짜 |
| category | TEXT | 분류 |
| item | TEXT | 항목 |
| shop | TEXT | 구매처 |
| price | INTEGER | 금액 |
| payment | TEXT | 결제수단 |

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

---

### settings

| Column | Type | Description |
|--------|------|-------------|
| key | TEXT | 설정 이름 |
| value | TEXT | 설정 값 (예: budget) |

```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

# 📷 화면

## 메인 Dashboard

<!-- ![메인 Dashboard](images/main.png) -->
<p align="center">
  <img src="images/main.png" width="500">
</p>

---

## 지출 등록 / 수정

<!-- ![지출 등록](images/expense_dialog.png) -->
<p align="center">
  <img src="images/expense_dialog.png" width="200">
</p>

---

## Excel Report

<!-- ### Summary Dashboard

![Excel Summary](images/excel_export_1.png)

### Detail Sheet

![Excel Detail](images/excel_export_2.png) -->

<p align="center">
  <img src="images/excel_export_1.png" width="500">
  <img src="images/excel_export_2.png" width="500">
</p>

---

## 통계 화면

<!-- ![통계](images/statistics.png) -->
<p align="center">
  <img src="images/statistics_1.png" width="500">
  <img src="images/statistics_2.png" width="500">
</p>

---

# 🗺 Roadmap

## Future Improvements

- [ ] Flutter 모바일 앱 개발
- [ ] 클라우드 데이터 동기화

---

# 📦 Version History

| Version | Description                                                                          |
| ------- | ------------------------------------------------------------------------------------ |
| v0.5.0 | 첫 번째 공식 Release / Dashboard UI 개선 / 검색·필터 기능 추가 / ExpenseDialog 분리 / 고유 ID 기반 데이터 관리 |
| v0.6.0 | Excel Report 기능 추가 / openpyxl 기반 Summary·Detail 시트 생성 / 지출 분석 Dashboard / 차트 기능 구현 |
| v0.7.0 | Dashboard UI 완성 / Card UI 적용 / 예산·지출·잔액 표시 / ExpenseDialog UI 개선 / 프로젝트 구조 정리 |
| v0.8.0 | 통계창 완성 / 최근 지출 TOP5 추가 / 버튼 및 레이아웃 개선 / 그래프 디자인 마무리 |
| v0.9.0 | SQLite 데이터베이스 적용 / JSON → SQLite 마이그레이션 / database.py 분리 / settings 테이블 추가 / DB 기반 CRUD 구현 |
| v1.0.0 | CSV Export / Database Backup & Restore / SQLite 데이터 관리 개선 / PyInstaller exe 배포 환경 구축 / 초기 DB 리소스 관리 / 사용자 DB 분리 / 배포 환경 안정화 |

---

# 📚 Documentation

프로젝트 개발 과정과 학습 내용은 아래 문서에 정리되어 있습니다.

* **development_log.md** : 개발 일지
* **study.md** : Python / Tkinter / openpyxl 학습 노트

---

# 👤 Developer

**Jiyoung Byeon**

WeddingMoneyManager는 결혼 준비 과정에서 발생하는 실제 지출 데이터를 관리하기 위해 개발한 개인 프로젝트입니다.

단순한 기능 구현을 넘어 Python GUI 프로그래밍(Tkinter), SQLite 데이터베이스 설계 및 CRUD 구현, 이벤트 처리, 객체 지향 설계, 모듈 분리, 데이터 시각화(Matplotlib), Excel 자동화(openpyxl), Windows 실행 파일 배포(PyInstaller) 등 실제 애플리케이션 개발 과정에서 필요한 기술을 학습하고 적용했습니다.