# Unit test class
import unittest
from function_extract_fields import extract_fields_recursive
class TestSQLFieldExtraction(unittest.TestCase):
    def test_query1(self):
        sql_query = """
        SELECT customer_id, city FROM orders GROUP BY customer_id, city
        """
        expected = [{'select_fields': ['customer_id', 'city'], 'group_by_fields': ['customer_id', 'city']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query2(self):
        sql_query = """
        SELECT customer_id, COUNT(other) FROM orders GROUP BY customer_id
        """
        expected = [{'select_fields': ['customer_id'], 'group_by_fields': ['customer_id']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query3(self):
        sql_query = """
        SELECT
            customer_id,
            (SELECT name FROM customers WHERE customers.id = orders.customer_id) AS customer_name,
            (SELECT SUM(amount) FROM payments WHERE payments.order_id = orders.id) AS total_payments
        FROM orders
        GROUP BY customer_id
        """
        expected = [{'select_fields': ['customer_id'], 'group_by_fields': ['customer_id']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query4(self):
        sql_query = """
        SELECT
            customer_id,
            city,
            SUM(amount) AS total_spent
        FROM orders
        GROUP BY customer_id, city
        ORDER BY total_spent DESC
        """
        expected = [{'select_fields': ['customer_id', 'city'], 'group_by_fields': ['customer_id', 'city']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query5(self):
        sql_query = """
        SELECT
            o.customer_id,
            c.city,
            AVG(o.amount) AS average_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        GROUP BY o.customer_id, c.city
        """
        expected = [{'select_fields': ['o.customer_id', 'c.city'], 'group_by_fields': ['o.customer_id', 'c.city']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query6(self):
        sql_query = """
        SELECT
            customer_id,
            (SELECT city FROM customers WHERE id = (SELECT customer_id FROM addresses WHERE addresses.customer_id = orders.customer_id)) AS customer_city
        FROM orders
        """
        expected = [{'select_fields': ['customer_id'], 'group_by_fields': []}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query7(self):
        sql_query = """
        SELECT
            customer_id,
            COUNT(*) AS num_orders
        FROM orders
        GROUP BY customer_id
        HAVING COUNT(*) > 5
        """
        expected = [{'select_fields': ['customer_id'], 'group_by_fields': ['customer_id']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query8(self):
        sql_query = """
        SELECT
            customer_id AS cid,
            MAX(amount) AS max_amount
        FROM orders
        GROUP BY cid
        """
        expected = [{'select_fields': ['cid'], 'group_by_fields': ['cid']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query9(self):
        sql_query = """
        SELECT
            CONCAT(first_name, ' ', last_name) AS full_name,
            customer_id
        FROM customers
        GROUP BY customer_id
        """
        expected = [{'select_fields': ['customer_id'], 'group_by_fields': ['customer_id']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)

    def test_query10(self):
        sql_query = """
        SELECT DISTINCT
            customer_id,
            city
        FROM orders
        GROUP BY customer_id, city
        """
        expected = [{'select_fields': ['customer_id', 'city'], 'group_by_fields': ['customer_id', 'city']}]
        result = extract_fields_recursive(sql_query)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
