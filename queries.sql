-- =====================================================
-- HR Attrition Analysis - SQL Queries
-- Dataset: IBM HR Analytics Employee Attrition (Kaggle)
-- Table name assumed: employees
-- =====================================================

-- 1. Overall attrition rate
SELECT
    Attrition,
    COUNT(*) AS employee_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM employees), 2) AS percentage
FROM employees
GROUP BY Attrition;


-- 2. Attrition rate by department
SELECT
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;


-- 3. Attrition rate by job role
SELECT
    JobRole,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY JobRole
ORDER BY attrition_rate_pct DESC;


-- 4. Attrition vs OverTime
SELECT
    OverTime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY OverTime;


-- 5. Attrition by tenure group
-- (Run this AFTER adding the TenureGroup column - see Step A below)
SELECT
    TenureGroup,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY TenureGroup
ORDER BY
    CASE TenureGroup
        WHEN '0-2' THEN 1
        WHEN '3-5' THEN 2
        WHEN '6-10' THEN 3
        WHEN '10+' THEN 4
    END;


-- 6. Average monthly income: stayed vs left, by job role
SELECT
    JobRole,
    Attrition,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    COUNT(*) AS employee_count
FROM employees
GROUP BY JobRole, Attrition
ORDER BY JobRole, Attrition;


-- 7. Attrition by job satisfaction level (1 = Low, 4 = Very High)
SELECT
    JobSatisfaction,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;


-- =====================================================
-- Step A: Add a TenureGroup column before running query 5
-- Run this once after importing the CSV (SQLite syntax)
-- =====================================================

ALTER TABLE employees ADD COLUMN TenureGroup TEXT;

UPDATE employees
SET TenureGroup = CASE
    WHEN YearsAtCompany <= 2 THEN '0-2'
    WHEN YearsAtCompany BETWEEN 3 AND 5 THEN '3-5'
    WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10'
    ELSE '10+'
END;
