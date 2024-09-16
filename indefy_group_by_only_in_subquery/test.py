# Unit test class
import unittest
from function import has_group_by_in_subquery
class TestHasGroupByInSubquery(unittest.TestCase):
    def test_group_by_in_subquery(self):
        sql = """
        SELECT *
        FROM (
            SELECT category, SUM(amount) AS total_amount
            FROM transactions
            GROUP BY category
        ) AS subquery
        """
        self.assertTrue(has_group_by_in_subquery(sql))

    def test_group_by_in_main_query(self):
        sql = """
        SELECT category, SUM(amount) AS total_amount
        FROM transactions
        GROUP BY category
        """
        self.assertFalse(has_group_by_in_subquery(sql))

    def test_no_group_by(self):
        sql = """
        SELECT *
        FROM transactions
        WHERE amount > 100
        """
        self.assertFalse(has_group_by_in_subquery(sql))

    def test_group_by_in_nested_subquery(self):
        sql = """
        SELECT *
        FROM (
            SELECT category, SUM(amount) AS total_amount
            FROM (
                SELECT category, amount
                FROM transactions
                WHERE amount > 100
            ) AS inner_subquery
            GROUP BY category
        ) AS outer_subquery
        """
        self.assertTrue(has_group_by_in_subquery(sql))

    def test_invalid_sql(self):
        sql = "SELECT * FROM tabl1"
        self.assertFalse(has_group_by_in_subquery(sql))


    def test1(self):
        sql = """
        SELECT category, total_amount
        FROM (
            SELECT category, SUM(amount) AS total_amount
            FROM transactions
            GROUP BY category
        ) AS subquery
        WHERE total_amount > 1000
        """
        self.assertTrue(has_group_by_in_subquery(sql))


    def test2(self):
        sql = """
        SELECT department, avg_salary
        FROM (
            SELECT department, AVG(salary) as avg_salary
            FROM employees
            GROUP BY department
            HAVING COUNT(*) > 5
        ) AS dept_stats
        WHERE avg_salary > 50000
        ORDER BY avg_salary DESC
        """
        self.assertTrue(has_group_by_in_subquery(sql))


    def test3(self):
        sql = """
        SELECT department, total_high_salaries
        FROM (
            SELECT department, SUM(high_salary) AS total_high_salaries
            FROM (
                SELECT department, AVG(salary) AS high_salary
                FROM employees
                GROUP BY department
                HAVING AVG(salary) > 75000
            ) AS high_salary_depts
            GROUP BY department
        ) AS dept_totals
        WHERE total_high_salaries > 500000
        ORDER BY total_high_salaries DESC
        """
        self.assertTrue(has_group_by_in_subquery(sql))


    def test4(self):
        sql = """
        SELECT 
            department,
            AVG(salary) AS avg_salary,
            (SELECT AVG(sub.salary)
            FROM employees sub
            WHERE sub.hire_date > '2020-01-01'
            AND sub.department = e.department
            GROUP BY sub.department) AS avg_new_hire_salary
        FROM employees e
        GROUP BY department
        HAVING COUNT(*) > 5
        ORDER BY avg_salary DESC
        """
        self.assertTrue(has_group_by_in_subquery(sql))

if __name__ == '__main__':
    unittest.main()