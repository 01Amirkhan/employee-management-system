create database EmployeeManagement;
USE  EmployeeManagement;


CREATE TABLE Department (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL
);

CREATE TABLE Employee (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    hire_date DATE,
    salary DECIMAL(10,2),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    date DATE,
    status ENUM('Present', 'Absent', 'Leave'),
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
);

INSERT INTO Department (dept_name) VALUES
('HR'),
('Finance'),
('IT'),
('Marketing');

INSERT INTO Employee (emp_name, email, phone, hire_date, salary, dept_id) VALUES
('Amit Sharma', 'amit@example.com', '9876543210', '2022-05-10', 50000.00, 1),
('Neha Singh', 'neha@example.com', '9123456780', '2021-08-22', 60000.00, 2),
('Rohit Jain', 'rohit@example.com', '9988776655', '2023-01-15', 55000.00, 3),
('Sonal Mehta', 'sonal@example.com', '9898989898', '2020-03-18', 65000.00, 4);

INSERT INTO Attendance (emp_id, date, status) VALUES
(1, '2025-08-01', 'Present'),
(1, '2025-08-02', 'Absent'),
(2, '2025-08-01', 'Present'),
(3, '2025-08-01', 'Leave'),
(4, '2025-08-01', 'Present');

select  * from Department;
select  * from Employee;
select  * from Attendance;

describe Attendance;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Employee') DEFAULT 'Employee',
    emp_id INT,
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id)
);

-- Insert sample users (passwords here are plain text for demo purposes; in real apps, store hashes)
INSERT INTO Users (username, password_hash, role, emp_id) VALUES
('admin', 'admin123', 'Admin', NULL),          -- Admin without linked employee
('amit', 'amitpass', 'Employee', 1),
('neha', 'nehapass', 'Employee', 2),
('rohit', 'rohitpass', 'Employee', 3),
('sonal', 'sonalpass', 'Employee', 4);

-- View the Users table

ALTER TABLE Users 
CHANGE COLUMN password_hash user_pwd VARCHAR(255) NOT NULL;

SELECT * FROM Users;






