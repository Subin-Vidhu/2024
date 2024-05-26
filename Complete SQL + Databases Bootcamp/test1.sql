--select dept_no, count(emp_no) from dept_emp group by dept_no order by dept_no;
--select dept_no, count(emp_no) from dept_emp group by dept_no having count(emp_no) > 50000 order by count;
--select dept_no, emp_no from dept_emp union select dept_no, emp_no from dept_emp;

-- SELECT hire_date, COUNT(emp_no) as "amount"
-- FROM employees
-- GROUP BY hire_date
-- ORDER BY "amount" DESC;

-- SELECT e.emp_no, count(t.title) as "amount of titles"
-- FROM employees as e
-- JOIN titles as t USING(emp_no)
-- WHERE EXTRACT (YEAR FROM e.hire_date) > 1991
-- GROUP BY e.emp_no
-- ORDER BY e.emp_no;

-- SELECT e.emp_no, de.from_date, de.to_date
-- FROM employees as e
-- JOIN dept_emp AS de USING(emp_no)
-- WHERE de.dept_no = 'd005'
-- GROUP BY e.emp_no, de.from_date, de.to_date
-- ORDER BY e.emp_no, de.to_date;

-- select dept_no, emp_no, count(emp_no) from dept_emp group by ROLLUP (dept_no, emp_no) order by dept_no;

-- select emp_no, salary, sum(salary) over () as total_salary from salaries order by emp_no;

SELECT emp_no, salary, max(salary) OVER (PARTITION BY emp_no) AS total_salary FROM salaries ORDER BY emp_no;