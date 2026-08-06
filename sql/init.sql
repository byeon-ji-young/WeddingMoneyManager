-- ==========================================
-- WeddingMoneyManager SQLite Database
-- 초기 테이블 생성 SQL
-- 프로그램 실행 시 database.py에서 생성
-- ==========================================

-- SQLite schema reference

-- ==========================================
-- 지출 내역 테이블
-- ==========================================
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    item TEXT NOT NULL,
    shop TEXT,
    price INTEGER NOT NULL,
    payment TEXT
);

-- ==========================================
-- 설정 테이블
-- 예산 등 프로그램 설정값 저장
-- ==========================================
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);