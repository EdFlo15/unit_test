import sqlglot

def has_group_by_in_subquery(sql_query):
    """
    Parses the given SQL query and checks if there is a GROUP BY clause specifically within subqueries.
    """
    # Parse the SQL query into an AST
    expression = sqlglot.parse_one(sql_query)
    
    def is_group_by_in_subquery(expr):
        """
        Recursively checks if there is a GROUP BY clause within subqueries.
        """
        # Check if the current node is a subquery
        if isinstance(expr, sqlglot.expressions.Subquery):
            # Check if this subquery contains a Group by clause
            if expr.find(sqlglot.expressions.Group):
                return True
            # Additionally check deeper in all parts of this subquery
            return any(is_group_by_in_subquery(sub_expr) for sub_expr in expr.this.args.values())
        
        # If not a subquery, recursively check all its parts
        if isinstance(expr, sqlglot.Expression):
            return any(is_group_by_in_subquery(sub_expr) for sub_expr in expr.args.values())
        
        return False

    # Start the recursive checking from the root of the AST
    return is_group_by_in_subquery(expression)
