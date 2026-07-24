# 💍 WeddingMoneyManager

결혼 준비 과정에서 발생하는 다양한 비용을 체계적으로 관리하기 위한  
**신혼 자금 관리 데스크톱 프로그램**입니다.

예식 준비, 혼수, 가전, 가구, 여행 등 결혼 과정에서 발생하는 지출을 기록하고  
예산 대비 사용 현황과 항목별 지출 분석을 한눈에 확인할 수 있도록 제작한 개인 프로젝트입니다.

---

## 📌 프로젝트 소개

결혼 준비 과정에서는 예식장, 가구, 가전, 생활용품, 여행 등 다양한 항목에서
큰 규모의 지출이 발생합니다.

WeddingMoneyManager는 이러한 비용을 직접 관리하기 위해 개발한 프로그램으로,
다음과 같은 목표를 가지고 제작했습니다.

* 결혼 준비 비용 기록
* 항목별 지출 관리
* 예산 대비 사용 금액 확인
* 지출 데이터 기반 통계 분석
* 실제 생활 데이터를 활용한 관리 프로그램 구현

---

## ✨ 주요 기능

### 💰 비용 관리
* 결혼 준비 비용 및 예산 등록
* 날짜 / 분류 / 항목 / 금액 기록
* 지출 내역 수정 및 삭제
* JSON 파일 기반 자동 데이터 저장 및 불러오기

### 📋 지출 관리
* Treeview 기반 지출 목록 표시
* 컬럼 클릭을 통한 항목별 정렬 (날짜, 분류, 항목, 금액)
* 실시간 키워드 검색 기능 제공 (항목명, 카테고리)

### 💳 예산 관리
* 전체 예산 설정 및 실시간 반영
* 현재 총 지출 금액 및 예산 대비 소진율(%) 계산
* 남은 금액 실시간 확인

### 📊 비용 분석
Matplotlib을 활용한 지출 데이터 시각화
* 카테고리별 지출 금액 비교 (막대그래프)
* 카테고리별 지출 비율 분석 (도넛형 원형그래프)

---

## 🛠 기술 스택

### Language
* Python 3.x

### GUI
* Tkinter, ttk

### Data Storage
* JSON

### Visualization
* Matplotlib

### External Library
* tkcalendar

### Development Environment
* Visual Studio Code
* Git / GitHub

---

## 📁 프로젝트 구조

```text
WeddingMoneyManager
│
├── main.py             # 메인 프로그램 소스코드
├── money.json          # 예산 및 지출 데이터 저장 파일 (자동 생성)
├── README.md           # 프로젝트 설명
└── requirements.txt    # 필요 패키지 목록
```

---

## ⚙ 실행 방법

### 1. 저장소 다운로드

```bash
git clone [https://github.com/username/WeddingMoneyManager.git](https://github.com/username/WeddingMoneyManager.git)
cd WeddingMoneyManager
```

### 2. 가상환경 생성

```bash
python -m venv venv
```

### 3. 가상환경 활성화

Windows:

```bash
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt (cmd)
.\venv\Scripts\activate.bat
```

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

### 5. 실행

```bash
python app.py
```

---

## 📷 화면 구성

추가 예정

* 메인 화면
* 비용 입력 화면
* 지출 관리 화면
* 통계 화면

---

## 🚀 개발 예정 기능

* 📅 월별 지출 분석
* 📈 비용 그래프 시각화
* 📄 엑셀 내보내기 기능
* ☁ 데이터 백업 기능
* 📱 모바일 환경 지원

---

## 📝 개발 목적

결혼 준비를 하면서 실제 발생하는 비용을 직접 관리하기 위해 시작한 프로젝트입니다.

단순한 가계부를 넘어 실제 생활 데이터를 기반으로 한 관리 프로그램 제작을 목표로 개발하고 있습니다.

---

## 👤 Developer

* Developer : Jiyoung Byeon
* Project : WeddingMoneyManager
