-- ==========================================================
-- Vikas Gupta Portfolio Database Schema (MySQL 5.7+ / 8.0+)
-- Database: vikas_portfolio_db
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `vikas_portfolio_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `vikas_portfolio_db`;

-- 1. Contacts Table (Stores inquiries submitted from portfolio contact form)
CREATE TABLE IF NOT EXISTS `contacts` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(120) NOT NULL,
    `email` VARCHAR(180) NOT NULL,
    `subject` VARCHAR(255) NOT NULL,
    `message` TEXT NOT NULL,
    `ip_address` VARCHAR(45) NULL,
    `user_agent` VARCHAR(255) NULL,
    `is_read` TINYINT(1) DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_email` (`email`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Projects Table (Allows dynamic projects management if stored in DB)
CREATE TABLE IF NOT EXISTS `projects` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(150) NOT NULL,
    `slug` VARCHAR(160) NOT NULL UNIQUE,
    `badge` VARCHAR(50) DEFAULT 'Full-Stack',
    `description` TEXT NOT NULL,
    `technologies` JSON NOT NULL,
    `features` JSON NOT NULL,
    `image_url` VARCHAR(255) NULL,
    `github_url` VARCHAR(255) NULL,
    `demo_url` VARCHAR(255) NULL,
    `display_order` INT DEFAULT 0,
    `is_published` TINYINT(1) DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed initial project showcase records
INSERT INTO `projects` (`title`, `slug`, `badge`, `description`, `technologies`, `features`, `image_url`, `github_url`, `demo_url`, `display_order`) VALUES
(
    'Product Management System',
    'product-management-system',
    'Laravel / PHP',
    'Comprehensive enterprise product management and inventory tracking web application built with Laravel and MySQL. Features full CRUD capabilities, SKU indexing, real-time inventory alerts, bulk data import/export, and image uploads with server-side validation.',
    '["Laravel", "PHP", "MySQL", "Bootstrap 5", "JavaScript"]',
    '["Product CRUD operations with image upload & file validation", "SKU tracking with low-stock alerts & stock level indicators", "Server-side search, filtering, and pagination", "CSV & Excel bulk product import and export engine", "Role-based access control for inventory managers"]',
    'images/project-product-mgmt.jpg',
    'https://github.com/VikasGupta2022',
    '#',
    1
),
(
    'HRMS / Employee Management System',
    'hrms-employee-management-system',
    'Laravel / Enterprise',
    'Robust Human Resource Management System engineered with Laravel & MySQL to automate employee lifecycle, attendance logs, timesheets, payroll calculations with tax and gratuity formulas, and comprehensive reporting.',
    '["PHP", "Laravel", "MySQL", "Bootstrap 5", "JavaScript", "Chart.js"]',
    '["Full employee directory with role and department assignments", "Daily attendance & timesheet logging with hours calculation", "Automated payroll generation with bonus and deduction rules", "Gratuity computation engine and financial report exports", "Employee training records, leave requests, and approval workflows"]',
    'images/project-hrms.jpg',
    'https://github.com/VikasGupta2022',
    '#',
    2
),
(
    'Student Management System',
    'student-management-system',
    'Core PHP / Portal',
    'Lightweight and high-efficiency student academic management portal constructed using Core PHP and MySQL with an MVC architecture pattern, offering course registration, attendance tracking, and reporting.',
    '["Core PHP", "MySQL", "HTML5", "CSS3", "Bootstrap", "JavaScript"]',
    '["Student records and profiles with enrollment history", "Course catalog and academic curriculum management", "Attendance marking system with percentage calculators", "Contact info directory with guardian details", "Clean MVC architecture and SQL prepared statements"]',
    'images/project-student-mgmt.jpg',
    'https://github.com/VikasGupta2022',
    '#',
    3
),
(
    'High-Performance Python REST API',
    'python-fastapi-rest-api',
    'Python / FastAPI',
    'Modern asynchronous RESTful microservice built with Python 3 and FastAPI, leveraging Pydantic v2 schemas for robust request validation, SQLAlchemy ORM with MySQL integration, and JWT authentication.',
    '["Python", "FastAPI", "MySQL", "Pydantic", "SQLAlchemy", "Uvicorn"]',
    '["Asynchronous endpoints for high-throughput CRUD operations", "Strong data validation and automatic serialization with Pydantic v2", "Interactive Swagger/OpenAPI and ReDoc self-documenting APIs", "JWT-based authentication and role-based route guards", "Robust database pooling with transactional integrity"]',
    'images/project-fastapi-api.jpg',
    'https://github.com/VikasGupta2022',
    '#',
    4
)
ON DUPLICATE KEY UPDATE `title` = VALUES(`title`);
