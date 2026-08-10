# 📒 WeddingMoneyManager 개발일지

---

## 📅 2026-07-23

### 프로젝트 초기 구축
- 가계부 프로그램 초기 버전 개발
- README.md 작성 및 프로젝트 설명 추가

### 데이터 목록 개선
- Listbox → Treeview 변경
- Treeview Index(iid) 기반 관리
- Treeview 컬럼 정렬 기능 추가

### 예산 관리
- 총 예산 입력 및 적용 기능 구현

### UI 개선
- Frame 구조 정리
- 버튼 UI 디자인 개선

---

## 📅 2026-07-24

### Dashboard UI 개선
- 대시보드 카드(Card) 디자인 적용
- ttk Theme 적용(clam)
- 예산 표시 위치 수정

### 레이아웃 개선
- 전체 Frame 구조 재배치
- pack() 기반 레이아웃으로 변경

### 문서
- README.md 내용 보완

---

## 📅 2026-07-27

### 입력 기능 개선
- 구매처 컬럼 추가
- 결제수단 컬럼 추가
- 금액 입력 시 자동 콤마 적용
- 입력 중 커서 위치 유지

### Dashboard 기능
- 예산 사용률 ProgressBar 추가
- 예산 사용량에 따른 색상 변경

### 검색 기능 개선
- 구매처 검색 지원
- 카테고리 필터 추가
- 결제수단 필터 추가

### 구조 개선
- 입력 팝업(ExpenseDialog) 모듈 분리
- 메인 실행 파일을 app.py → main.py 변경

### 수정 기능 개선
- 수정 팝업 자동 데이터 채움
- 수정 후 선택 행 유지

### 추가 기능 개선
- 추가 후 새로 등록한 행 자동 선택

### 예외 처리
- 데이터가 없을 경우 안내 메시지 표시

---

## 📅 2026-07-28

### 데이터 구조 개선
- Treeview의 `iid`를 Index 기반에서 고유 ID 기반으로 변경
- 모든 데이터에 고유 ID 자동 생성 로직 추가
- 기존 데이터도 ID가 없으면 자동 생성되도록 개선
- 수정 시 기존 ID를 유지하도록 변경
- 삭제 시 Index에 의존하지 않는 구조로 개선

### 릴리즈
- Release **v0.5.0** 생성
- 그래프 기능은 UI 개선 예정으로 임시 비활성화

### 엑셀
- 엑셀 파일 생성 기능 구조 개선
- 기존 `excel_manager.py`에서 스타일, 상세내역, 분석 시트 생성 기능 분리
  - `excel/styles.py` : 엑셀 스타일(폰트, 색상, 테두리, 정렬) 관리
  - `excel/detail.py` : 지출내역 시트 생성 담당
  - `excel/summary.py` : 대시보드(분석) 시트 생성 담당
- 엑셀 Export 로직을 `excel_exporter.py`로 변경하여 시트 생성 흐름 관리
- 기존 지출내역 시트 디자인 유지 및 스타일 코드 중복 제거
- 결혼 준비 비용 분석을 위한 대시보드 시트 추가
  - 예산 사용률 표시
  - 카테고리별 지출 분석
  - 최대 지출 TOP 5 표시
  - 결제수단별 지출 분석
- summary 전용 스타일 추가 및 카드 형태 UI 적용
- 병합 셀 스타일 적용을 위한 공통 `style_range()` 함수 추가

---

## 📅 2026-07-29

### Excel Report 기능 개선

#### 구현 내용
- openpyxl 기반 Excel 리포트 생성 기능 추가
- 요약 시트 구성
- 상세 지출 내역 시트 구성
- 카테고리별 지출 차트 추가
- 월별 지출 추이 LineChart 추가
- 요약 카드 UI 적용

#### 디자인 개선
- 차트 스타일 수정
- 데이터 라벨 위치 조정
- LineChart 색상 통일
- Excel 셀 스타일 모듈화

#### 사용 기술
- openpyxl

### 릴리즈
- Release **v0.6.0** 생성

---

## 📅 2026-08-03

### UI 개선

#### 디자인 개선
- 지출 등록/수정 팝업 UI 리뉴얼
- 팝업 내부 타이틀 추가
- 기본 정보 / 결제 정보 영역 분리
- ttk.LabelFrame 기반 그룹 UI 적용
- 입력 영역 여백 및 크기 개선
- 저장 / 취소 버튼 디자인 개선

#### 스타일 개선
- ttk 스타일 설정 추가
- Combobox 스타일 통일
- DateEntry 스타일 적용
- 전체 팝업 색상 및 폰트 디자인 통일

#### 구조 개선
- 전달받은 title 값을 팝업 내부 제목으로 활용하도록 개선
- UI 생성 코드 구조 정리

---

### 프로젝트 정리

- Excel Report 기능 및 UI 개선 완료
- v0.6.0 이후 UI 개선 사항 반영

### 릴리즈
- Release **v0.7.0** 생성

--- 

## 📅 2026-08-04

### UI 개선 및 Dashboard 완성

#### Added
- Dashboard 화면 구성 완료
- 예산 / 총 지출 / 잔액 Card UI 추가
- 예산 사용률 표시 기능 추가
- 카테고리별 지출 분석 그래프 추가
- 결제수단별 지출 분석 그래프 추가
- 최근 지출 TOP5 표시 기능 추가

#### UI 개선
- 기존 Treeview 중심 화면에서 Dashboard 형태로 변경
- 화면 레이아웃 재구성
- 입력 영역과 데이터 표시 영역 개선
- 버튼 및 주요 UI 요소 스타일 통일
- 전체적인 화면 가독성 개선

#### Chart 개선
- Matplotlib 그래프 UI 개선
- 카테고리별 막대그래프 개선
- 신혼자금 사용 비율 파이차트 추가
- 한글 폰트 표시 문제 개선

#### Release
- Release **v0.8.0 생성**
- 통계 화면 및 Dashboard UI 개선 완료

---

## 📅 2026-08-06

### SQLite 저장 방식 적용

#### Added
- SQLite 데이터베이스 저장 방식 적용
- expenses 테이블 CRUD 기능 구현
- settings 테이블 추가
- 예산(Budget) 설정 DB 저장 기능 추가
- JSON → SQLite 데이터 마이그레이션 스크립트 추가 (`migrate_json_to_sqlite.py`)
- 데이터베이스 초기 생성 기능 추가

#### Changed
- 기존 JSON 저장 방식에서 SQLite 저장 방식으로 변경
- 지출 추가/수정/삭제 로직을 SQLite 기반으로 변경
- 프로그램 시작 시 DB에서 데이터 및 예산 자동 로드
- 예산 변경 시 settings 테이블에 즉시 저장하도록 변경

#### Refactored
- 데이터 접근 로직을 `database.py`로 분리
- UI와 데이터 처리 로직 분리
- CRUD 함수 구조 개선
- 프로그램 구조 정리 및 코드 가독성 향상

#### Backup
- JSON 기반 이전 버전 백업
- 기존 app.py / main.py 백업 파일 정리

#### Release
- Release **v0.9.0 생성**
- SQLite 기반 데이터 저장 방식 적용 완료

---

### SQLite 데이터 관리 기능 개선

#### Added
- CSV Export 기능 추가
- SQLite Database Backup 기능 추가
- SQLite Database Restore 기능 추가
- 복원 전 기존 데이터 자동 백업 처리
- 검색 결과 건수 표시 기능 추가

#### Improvement
- 데이터 관리 안정성 개선
- 사용자 데이터 보호 기능 강화
- 버튼 UI 및 레이아웃 개선

#### Refactoring
- 데이터 관리 기능 구조 정리
- Backup / Restore 기능 모듈 분리

---

## 📅 2026-08-07

### Windows 실행 파일 배포 환경 개선

#### Added
- PyInstaller 기반 exe 빌드 환경 구성
- `WeddingMoneyManager.spec` 파일 추가 및 빌드 설정 관리
- exe 아이콘 적용
- 배포용 초기 SQLite DB 리소스 추가

#### Changed
- exe 실행 환경에서 SQLite DB 경로 처리 방식 개선
- PyInstaller 내부 리소스(`_internal/wedding.db`)를 초기 DB 템플릿으로 사용
- 최초 실행 시 초기 DB를 사용자 영역 DB로 복사하는 구조 적용
- 기존 데이터 유지가 가능하도록 DB 초기화 로직 개선

#### Resource
- 초기 배포용 DB를 `resources/wedding.db`로 분리
- Git에서 관리되는 템플릿 DB와 실행 후 생성되는 사용자 DB 구분
- `.gitignore` 예외 설정을 통해 템플릿 DB 관리

#### Build
- PyInstaller `onedir` 방식 적용
- spec 파일 기반 빌드 방식으로 변경
- 빌드 결과물 구조 정리

#### Release
- Release **v1.0.0 준비**
- Windows exe 배포 환경 구성 완료

---

## 📅 2026-08-07 ~ 2026-08-10

### Category Management

#### Added

* SQLite `categories` 테이블 추가
* 카테고리 관리 창(`CategoryWindow`) 추가
* 카테고리 추가 / 수정 / 삭제(CRUD) 기능 구현
* 지출 등록 / 수정 창의 카테고리를 데이터베이스와 연동

#### Improvement

* 중복 카테고리 추가 방지
* 사용 중인 카테고리 삭제 방지
* 카테고리 관리 UI 개선
* MessageBox 부모 창(`parent`) 지정으로 UI 안정성 개선

#### Refactoring

* Category 관련 데이터 접근 로직 분리 (`database/category.py`)
* 카테고리 조회 함수 분리 (`get_category_list`, `get_all_categories`)
* 프로젝트 패키지 구조 개선

  * `database/`
  * `ui/`
  * `utils/`
  * `excel/`
* 기존 `backup/` 폴더를 `archive/` 폴더로 변경

---

### Settings 기능 추가

#### Added

* 설정 창(`SettingsWindow`) 추가
* 설정 창에서 예산 관리 기능 제공
* 예산 설정을 별도의 `BudgetDialog`로 분리
* 설정 창에서 카테고리 관리 기능 연결
* 설정 창에서 CSV Export 기능 연결
* 설정 창에서 Database Backup 기능 연결
* 설정 창에서 Database Restore 기능 연결

#### Improvement

* 예산 변경 시 Database의 `settings` 테이블에 즉시 저장
* 예산 변경 후 Dashboard의 예산 및 잔액 정보 자동 갱신
* Settings → BudgetDialog → Main Dashboard 간 Callback 구조 적용
* 설정 창을 Modal Window로 구성하여 메인 화면과 동시에 조작할 수 없도록 개선

#### Refactoring

* 설정 화면과 예산 입력 화면의 역할 분리
* `SettingsWindow`와 `BudgetDialog` 간 기능 연결 구조 개선
* 설정 관련 UI 코드 분리 및 관리

---

### Database Backup / Restore 안정성 개선

#### Added

* Database Restore 전 파일 유효성 검증 기능 추가
* 잘못된 `.db` 파일 선택 시 복원 차단
* SQLite Database가 아닌 파일 선택 시 복원 차단
* WeddingMoneyManager에서 필요한 Database 구조가 없는 경우 복원 차단

#### Improvement

* Database Restore 실행 전 현재 사용자 DB 자동 백업
* 복원 완료 후 프로그램 재실행 안내
* 복원 과정에서 사용자 데이터가 잘못된 Database로 덮어써지는 문제 방지
* Backup / Restore 기능의 예외 상황 처리 강화

#### Test

* 정상적인 SQLite Database 복원 테스트
* 잘못된 `.db` 파일 복원 테스트
* SQLite Database가 아닌 파일 복원 테스트
* Restore 전 기존 DB Backup 생성 테스트
* Restore 완료 후 프로그램 종료 및 재실행 테스트

---

### CSV Export

#### Improvement

* Settings 창에서 CSV Export 기능 연결
* 지출 데이터를 CSV 파일로 저장
* Excel에서 한글이 깨지지 않도록 `utf-8-sig` 인코딩 적용
* 저장 위치를 사용자가 직접 선택할 수 있도록 File Dialog 적용

---

### UI 개선

#### Improvement

* 전체 UI 디자인 개선
* Settings Window UI 구성
* Budget Dialog UI 구성
* Category Window UI 개선
* 버튼 및 입력 영역 디자인 통일
* Settings Window Modal 처리
* MessageBox의 부모 창 지정으로 팝업 표시 안정성 개선

---

### Project Structure

기능 확장에 따라 프로젝트 코드를 역할별 패키지로 분리하였다.

```text
WeddingMoneyManager
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

#### 역할 분리

* `database/` → SQLite 연결 및 데이터 CRUD
* `ui/` → Tkinter 화면 및 사용자 인터페이스
* `utils/` → CSV Export / Database Backup & Restore
* `excel/` → Excel Report 생성 및 스타일 관리

기존 하나의 파일에 집중되어 있던 기능을 역할별 패키지로 분리하여 유지보수성과 확장성을 개선하였다.

---

### Release

* Release **v1.1.0 생성**
* Category Management 기능 추가
* Settings 기능 추가
* Database Backup / Restore 안정성 개선
* Database Restore 파일 검증 기능 추가
* 프로젝트 패키지 구조 개선
* UI 개선 및 기능별 모듈 분리 완료
