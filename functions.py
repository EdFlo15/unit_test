import sqlglot

def modify_sql_query(sql_query, condition_to_remove):
    expression = sqlglot.parse_one(sql_query)
    def remove_condition(exp):
        if isinstance(exp, sqlglot.expressions.And):
            left_matches = exp.left.sql().strip().lower() == condition_to_remove.lower()
            right_matches = exp.right.sql().strip().lower() == condition_to_remove.lower()
            if left_matches and right_matches:
                return None
            elif left_matches:
                return exp.right
            elif right_matches:
                return exp.left
        elif isinstance(exp, sqlglot.expressions.Where):
            # If the condition matches exactly and there are no other conditions, remove the WHERE clause
            if exp.this.sql().strip().lower() == condition_to_remove.lower():
                return None
        return exp

    # Modify the AST by removing the specified condition
    modified_expression = expression.transform(remove_condition)

    # If the entire WHERE clause was removed, remove the WHERE keyword from the final SQL
    result_sql = modified_expression.sql()
    if "WHERE" in result_sql.upper() and "WHERE" == result_sql.strip()[-5:].upper():
        result_sql = result_sql.replace(" WHERE", "")  # Remove dangling WHERE

    return result_sql
