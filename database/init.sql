CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100),
    salary DECIMAL(10,2)
);

INSERT INTO employees(name,email,department,salary)
VALUES
('Sainath','sainath@gmail.com','DevOps',55000),
('Rahul','rahul@gmail.com','Cloud',60000),
('Priya','priya@gmail.com','Testing',45000),
('Amit','amit@gmail.com','HR',50000),
('vishal','vishal@gmail.com','Marketing',40000);