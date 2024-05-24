--select * FROM "employees";
--select * FROM "departments";
--select * from "salaries";
--select * FROM "titles";

-- select emp_no as "Employee #", birth_date as "Bday" FROM "employees";

--select concat( emp_no, 'is a ', title )AS "Employee Title" FROM titles;
--SELECT concat( first_name ,' ', last_name) as "Full_Name" from "employees";

--select count(emp_no) from employees;
--select sum(salary) from salaries;

-- SHOW timezone;
--select current_setting('TIMEZONE');

--select current_date;

--select extract(year from age(birth_date)) from employees;
SELECT age(birth_date) FROM employees;

