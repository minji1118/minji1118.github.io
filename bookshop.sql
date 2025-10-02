CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- 회원 테이블
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 책 테이블
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    price INT NOT NULL
);

-- 판매 테이블
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT DEFAULT 1,
    total_price INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 샘플 책 데이터
INSERT INTO books (title, price) VALUES
('파이썬 입문', 15000),
('C++ 객체지향', 20000),
('데이터베이스 기초', 18000);
