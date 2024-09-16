import unittest
import sqlglot
from functions import modify_sql_query

class TestModifySQLQuery(unittest.TestCase):

    def test_remove_simple_condition(self):
        sql_query = "SELECT * FROM products WHERE price > 100 AND quantity < 50 AND quality='good'"
        condition_to_remove = "price > 100"
        expected = "SELECT * FROM products WHERE quantity < 50 AND quality = 'good'"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_condition_with_numeric(self):
        sql_query = "SELECT * FROM sales WHERE amount = 300 AND taxes=50"
        condition_to_remove = "amount = 300"
        expected = "SELECT * FROM sales WHERE taxes = 50"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_string_condition(self):
        sql_query = "SELECT * FROM people WHERE name = 'John Doe' AND surname='FLORES'"
        condition_to_remove = "name = 'John Doe'"
        expected = "SELECT * FROM people WHERE surname = 'FLORES'"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_function_condition(self):
        sql_query = "SELECT * FROM events WHERE year(start_date) = 2022 AND MONTH='01'"
        condition_to_remove = "year(start_date) = 2022"
        expected = "SELECT * FROM events WHERE MONTH = '01'"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_complex_condition(self):
        sql_query = "SELECT * FROM logs WHERE error_code = 500 AND (status = 'fail' OR retry = true)"
        condition_to_remove = "error_code = 500"
        expected = "SELECT * FROM logs WHERE (status = 'fail' OR retry = TRUE)"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_condition_in_and(self):
        sql_query = "SELECT * FROM orders WHERE item = 'Widget' AND quantity = 10 AND price < 20"
        condition_to_remove = "item = 'Widget'"
        expected = "SELECT * FROM orders WHERE quantity = 10 AND price < 20"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_condition_with_date(self):
        sql_query = "SELECT * FROM records WHERE date = '2021-12-25'"
        condition_to_remove = "date = '2021-12-25'"
        expected = "SELECT * FROM records"  # Expected to remove everything from the WHERE clause
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_in_operator(self):
        sql_query = "SELECT * FROM users WHERE id IN (1, 2, 3) AND city='CALI'"
        condition_to_remove = "id IN (1, 2, 3)"
        expected = "SELECT * FROM users WHERE city = 'CALI'"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_exists_condition(self):
        sql_query = "SELECT * FROM users WHERE exists (SELECT id FROM orders WHERE user_id = users.id) AND SALES=1"
        condition_to_remove = ""
        expected = "SELECT * FROM users WHERE EXISTS(SELECT id FROM orders WHERE user_id = users.id) AND SALES = 1"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_condition_with_join_and_multiple_conditions(self):
        sql_query = "SELECT u.name, o.order_date FROM users u JOIN orders o ON u.id = o.user_id WHERE u.age > 18 AND o.total > 100 AND u.country = 'USA'"
        condition_to_remove = "u.age > 18"
        expected = "SELECT u.name, o.order_date FROM users AS u JOIN orders AS o ON u.id = o.user_id WHERE o.total > 100 AND u.country = 'USA'"
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

    def test_remove_only_condition(self):
        sql_query = "SELECT name, email FROM customers WHERE status = 'active'"
        condition_to_remove = "status = 'active'"
        expected = "SELECT name, email FROM customers"  # Expected to remove the entire WHERE clause
        result = modify_sql_query(sql_query, condition_to_remove)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
